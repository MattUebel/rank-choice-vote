from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List

# Create the FastAPI instance
app = FastAPI()

# Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

# ----------------------------
# In-memory "database"
# ----------------------------
candidates: List[str] = []
ballots: List[List[str]] = []
election_open: bool = False
round_number: int = 0


def ranked_choice_voting(ballots: List[List[str]]) -> (str, int):
    """
    Implements a simple Ranked-Choice Voting (Instant-Runoff).
    Returns the name of the winning candidate and the number of votes the winner won with.
    """
    # Gather a set of all candidates from all ballots
    active_candidates = list({cand for ballot in ballots for cand in ballot})

    while True:
        # Tally first-place votes for active candidates
        vote_counts = {cand: 0 for cand in active_candidates}

        for ballot in ballots:
            for choice in ballot:
                if choice in active_candidates:
                    vote_counts[choice] += 1
                    break

        total_votes = sum(vote_counts.values())

        # Check for majority (> 50%)
        for cand, count in vote_counts.items():
            if count > total_votes / 2:
                return cand, count  # Found a winner

        # Identify candidates with the fewest votes
        min_votes = min(vote_counts.values())
        lowest_candidates = [c for c, ct in vote_counts.items() if ct == min_votes]

        # Remove one candidate with the fewest votes (simple approach)
        if lowest_candidates:
            active_candidates.remove(lowest_candidates[0])

        # If only one candidate remains, they are the winner
        if len(active_candidates) == 1:
            return active_candidates[0], vote_counts[active_candidates[0]]


@app.get("/", response_class=HTMLResponse)
async def home():
    """
    Redirect to /start automatically.
    """
    return RedirectResponse(url="/start")


@app.get("/start", response_class=HTMLResponse)
async def get_start(request: Request):
    """
    Page to input a comma-delimited list of candidates.
    """
    return templates.TemplateResponse("start.html", {"request": request})


@app.post("/start", response_class=HTMLResponse)
async def post_start(
    request: Request,
    candidate_list: str = Form(...),
):
    """
    Handles the creation of a new election, resetting global state.
    """
    global candidates, ballots, election_open, round_number

    # Reset in-memory data
    candidates = []
    ballots = []
    election_open = False
    round_number = 0

    # Parse input
    raw_candidates = [c.strip() for c in candidate_list.split(",") if c.strip()]
    if len(raw_candidates) != len(set(raw_candidates)):
        return templates.TemplateResponse("start.html", {"request": request, "error": "Duplicate candidates are not allowed."})
    if raw_candidates:
        candidates = raw_candidates
        election_open = True
        return RedirectResponse(url="/vote", status_code=303)
    else:
        # If no valid candidates, stay on start page
        return templates.TemplateResponse("start.html", {"request": request})


@app.get("/vote", response_class=HTMLResponse)
async def get_vote(request: Request):
    """
    Displays the voting page with three dropdowns for ranks.
    If election is not open, redirect to /start.
    """
    if not election_open:
        return RedirectResponse(url="/start")

    return templates.TemplateResponse(
        "vote.html", {"request": request, "candidates": candidates}
    )


@app.post("/vote", response_class=HTMLResponse)
async def post_vote(
    request: Request,
    rank1: str = Form(...),
    rank2: str = Form(...),
    rank3: str = Form(...),
):
    """
    Processes the submitted ballot and appends it to the ballots list.
    Then redirects back to /vote so more ballots can be cast or the election can be closed.
    """
    if not election_open:
        return RedirectResponse(url="/start")

    if len({rank1, rank2, rank3}) < 3:
        return templates.TemplateResponse("vote.html", {"request": request, "candidates": candidates, "error": "Duplicate choices are not allowed."})

    global ballots
    ballots.append([rank1, rank2, rank3])
    return RedirectResponse(url="/vote", status_code=303)


@app.get("/close", response_class=HTMLResponse)
async def close_election():
    """
    Closes the election, then redirects to /results.
    """
    global election_open
    election_open = False
    return RedirectResponse(url="/results")


@app.get("/results", response_class=HTMLResponse)
async def results(request: Request):
    """
    Displays the winner (if any) and a button to start a new election.
    If the election is still open, redirect to /vote.
    """
    if election_open:
        return RedirectResponse(url="/vote")

    if not candidates or not ballots:
        winner = "No valid winner (no candidates or no ballots)."
        winner_votes = 0
    else:
        winner, winner_votes = ranked_choice_voting(ballots)

    return templates.TemplateResponse(
        "closed.html", {"request": request, "winner": winner, "round_number": round_number, "winner_votes": winner_votes}
    )
