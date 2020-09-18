# DB Migration

This is the directory to setup the initial DB and seed it with the training data in the provided csv.

## TODO

1. What is the edited_at column in incidents table?
2. New evidence table.
3. What is the `spatial_ref_sys` table?
4. Delete `evidence_dim`, `evidence` and stick with `evidences`
5. Populate the entries in `tags_ref` into `tags`.
6. Make sure `incidents` correctly references to places during seeding.

## Incident ma-springfield-42 @ Springfield, MA

Query entire places table and put into dictionary and check if Springfield is already.

If springfield:
check if incident id is greater than incident count
else:
create springfield record in places table

add incident

Check evidence

- Query entire incidents table, and check evidence counts at each one
