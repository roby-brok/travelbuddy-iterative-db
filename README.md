# TravelBuddy - Iterative DB Lab

**Module:** SWE6301 Agile Programming, Week 9: Iterative DB Engineering
**Activity:** Evolving the Foundation: Iterative Database Engineering and Schema Migrations
**Team:** Adrian, Blagoy, Roberto Cassano Brocato
**Branch:** all the lab work is on `iterative-db-lab`

In this lab we grow the TravelBuddy database in small steps with Django migrations, instead of designing it all up front. We add a field without breaking anything, test a rollback, and split `destination` into `city` and `country` without losing any data.

## Migration history

| Migration | Type | Change | Breaking? | Commit |
|---|---|---|---|---|
| `0001_initial` | schema | create `Trip` (`destination`, `start_date`) | - | SETUP |
| `0002_trip_budget` | schema | add `budget` (`null=True, blank=True`) | no | ADD |
| `0003_add_city_country` | schema | add `city` and `country`, make `destination` optional | no | UPDATE |
| `0004_split_destination` | data | copy "Paris, France" into `city` "Paris" and `country` "France" (and join them back on rollback) | no | UPDATE |
| `0005_remove_trip_destination` | schema | remove `destination` | yes | UPDATE |

Commits on the branch: SETUP -> ADD -> TEST -> UPDATE -> REFLECT.

## Structure

```
travelbuddy-iterative-db/
├── config/                  # Django project settings
├── travelbuddy/
│   ├── migrations/          # 0001-0005, the history of the database
│   └── models.py            # the Trip model
├── evidence/                # real command output for each phase
├── docs/
│   └── REFLECTION.md        # answers to the review questions
├── show_table.py            # prints the columns and rows of the trip table
├── manage.py
└── requirements.txt
```

## Run it

You need Python 3.12 or newer.

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows  (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
python manage.py migrate
```

`db.sqlite3` is not in Git, so a fresh clone starts with an empty table.

## Rollback test

```bash
python manage.py showmigrations travelbuddy    # find the last migration
python manage.py migrate travelbuddy 0001      # roll back the budget change
python show_table.py                           # budget column is gone
python manage.py migrate                       # forward again to the latest state
```

The same works for the whole split: `python manage.py migrate travelbuddy 0002` brings `destination` back with the original text, and `python manage.py migrate` splits it again.

## See the data migration run

On a database that has trips in it:

```bash
python manage.py migrate travelbuddy 0003      # undo the split, destination comes back
python manage.py migrate                       # apply 0004 (data) and 0005 again
python show_table.py                           # trips now have city and country
```

## Evidence

| File | Phase |
|---|---|
| `evidence/01_setup.txt` | first migration and the sample trips |
| `evidence/02_add_budget.txt` | non-breaking `budget` field, old trips still work |
| `evidence/03_rollback_test.txt` | rollback to 0001 and forward again |
| `evidence/04_data_migration.txt` | city/country split, rollback test of the split |
