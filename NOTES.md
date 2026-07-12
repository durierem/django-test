# Some notes that gather my thinking

## Foreword

Please, note that my main experience is with using Ruby on Rails so I used this exercise to learn
and explore Django along the way. Consider my small experience with the framework when reviewing
this code. In any case, whatever the framework, web dev is still web dev, and I found very similar
fundamental issues and patterns.

## Actual notes

App name : operations

A BusStop is a place. A Place can be a BusStop, but also eventually other types such as TrainStop
for example. Having BusStop, and TrainStop as separate tables enable this multiplicity of function
for the same place.

BusStop order is determined by arrival time, no need for an additional order column.

One can be tempted to add departure_bus_shift_entry and arrival_bus_shift_entry to BusShift to
enforce it having at least two stops but it de-normalizes the data and create duplication with what
can already be determined with the set en entries. I think adding a validation only at the database
level is sane as it also enables to have a "WIP" shift.

We might want to denormalize (arrival_time/duration) instead of recomputing things on the go, but
only if we actually hit performance issues. Correctness is more important than speed.

To add proper database constraints, one could use PostgreSQL with the `tstzrange` type
(https://www.postgresql.org/docs/current/rangetypes.html) or compile SQLite with the R*Tree module
(https://sqlite.org/draft/rtree.html). Speaking with some experience in compiling and deploying
custom SQLite distributions for [MTG Translator](https://mtg-translator.net), I don't really want to
go into this trouble for the exercise, but it's a good thing to know.

Simlpified `__str__` representation so that it's more natural to read about on the admin interface
and it avoids some N+1 queries.

I'm fighting a bit with N+1 queries in the admin that are _everywhere_. Having to use custom
querysets to preload data and fix the issue kinda defeat the purpose of an easy to use admin
interface builder and I feel like Django could improve a lot on that. Coming from Rails, I didn't
expected this to be so convoluted. I like the concept of query Managers though.
EDIT: I think I've come to a satisfying solution with using different managers in different contexts
and letting the caller (that knows what objects and attributes thet want) to use the appropriate
context manager

I'm also having some troubles with the validation. There are multiple ways of validating in Django.
Which is the right one? I've decided on considering the shift overlap and minimum number of stops as
business specific validation that do not pose a risk on data integrity and as such I don't want to
force a complex validation at the database or model level and it's the caller's responsibility to
validate business rules. In our case, it's the Admin interface using a custom FormSet with a clean()
method that does the heavy lifting. It could be refactored into a dedicated Validator to use in
other places.
