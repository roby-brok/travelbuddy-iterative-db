# Iterative DB Lab Reflection

**Team:** Adrian, Blagoy, Roberto Cassano Brocato

Here we answer the review questions about how we grew the TravelBuddy database in small steps.

---

## 1. How does maintaining a versioned migration history act as "unambiguous documentation" of the database's evolution?

Our `travelbuddy/migrations` folder tells the whole story of the Trip table, one step at a time:

| Migration | What it did | Commit |
|---|---|---|
| `0001_initial` | created Trip with `destination` and `start_date` | SETUP |
| `0002_trip_budget` | added an optional `budget` | ADD |
| `0003_add_city_country` | added `city` and `country`, made `destination` optional | UPDATE |
| `0004_split_destination` | copied the data from `destination` into `city` and `country` | UPDATE |
| `0005_remove_trip_destination` | removed `destination` | UPDATE |

If you read these five files in order, you know exactly how the table got to its current shape. Git adds the when and the why, because every migration sits in a commit with a clear message.

It is unambiguous because the migrations are the code that builds the database. A Word data dictionary can say one thing while the real database says another, and then the document is the "complicated lie" from the lecture. Migrations can't drift like that. If a migration file is wrong, `migrate` fails or the table comes out wrong, and we see it straight away. `python manage.py showmigrations` also shows which state any copy of the database is in, with `[X]` for applied and `[ ]` for not applied. A new team member doesn't need to ask anybody. They clone the repo, run `migrate`, and get the same database as the rest of us. This follows the Law of Documentation: we didn't write any extra document, because the migrations already are the documentation, and they are always up to date.

## 2. Robert Martin notes that "Rigidity" makes a design hard to change. How do automated migrations help our team overcome the rigidity typically associated with databases?

A design is rigid when one change causes a cascade of other changes. The database is often the most rigid part of a system. Changing a table by hand means writing SQL, running it on every laptop and on the server, and hoping nobody forgets a step. So teams avoid touching it, and the schema starts to rot.

Migrations make a change small and routine. For `budget` we changed one line in `models.py`, ran `makemigrations` and `migrate`, and that was it. The same file runs the same way on every machine, so the rest of the team only has to pull and run `migrate`.

The rollback is the other half. We tested every change backwards and forwards (`evidence/03_rollback_test.txt` and `evidence/04_data_migration.txt`). Because we know we can go back, we are not afraid to change the schema, and that is what takes the rigidity away. The city/country split shows this best. It was a breaking change, but we did it in three small migrations (add the new fields, move the data, remove the old field) and we never lost a trip. The rollback test even found a rigid spot for us. With `destination` still required, rolling back the split crashed with `NOT NULL constraint failed`. We found it in a throwaway copy on a laptop, not on a live system, and we fixed it before the real change.

## 3. Why is "Simplicity" (maximizing the amount of work not done) important when deciding whether to add complex database constraints early in a project?

For a database, simplicity means we only add the tables, columns and rules that the current story needs (YAGNI). Every constraint is a guess about the future. If the guess is wrong, we need another migration to undo it, and maybe we need to fix the data too. That is rework, so it is waste (Muda).

We saw this in our own lab. In the first model `destination` was a required field. When the customer asked for city and country, that rule made the change harder: before we could remove the field, we had to make it optional, or the rollback would crash. If we had also added rules like one trip per destination per date, or a fixed list of countries, there would be even more to undo.

Constraints also block the non-breaking path. Our `budget` change was easy only because the new column was optional. A required `budget` would need a value for every old trip, and the old code that saves trips without a budget would break.

This doesn't mean no rules at all. `start_date` is required, because every trip needs one today. The idea is to add a constraint when a story really needs it, as its own small migration with its own rollback test, instead of guessing at the start. A simple schema is easy to change, and a schema that is easy to change can follow the customer instead of rotting.
