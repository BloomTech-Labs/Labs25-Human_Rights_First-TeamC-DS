# DB Migration

This is the directory to setup the initial DB and seed it with the training data in the provided csv.

## TODO
- [ ] Make sure `incidents` correctly references to places during seeding.
- [x] ~~What is the edited_at column in incidents table?~~
- [x] What is the `spatial_ref_sys` table? (Delete it)
- [x] ~~Delete `evidence_dim`, `evidence` and stick with `evidences`.~~
- [ ] Populate the entries in `tags_ref` into `tags`. 
- [ ] Delete `tags_ref` and `tags_junction`
- [ ] Delete `place` and `incident_dim` tables
- [ ] Remove pprint imports from files?

## Incident ma-springfield-42 @ Springfield, MA

Query entire places table, put it into a dictionary, and check if Springfield is in it.

If springfield:
check if incident id is greater than incident count
else:
create springfield record in places table

add incident

Check evidence

- Query entire incidents table, and check evidence counts at each one
