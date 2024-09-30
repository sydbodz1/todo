## How to run

### Prerequisites

Before you begin, ensure you have [docker](https://www.docker.com/get-started/) installed

Once the project is unzipped, navigate to the root of this directory and run:

```
docker compose up
```

or optionally if you would like automatic rebuilding when you make changes, you can run:

```
docker compose watch
```

once running, navigate to localhost:8000/docs to see the docs, or POST to any of the defined endpoints!

## Decisions

### Why postgresql?
I decided to use a relational database for this because there were already a couple of identifiers that we'd want to easily select from (`taskIdentifier` and `event_id`). This use case also feels like it might eventually want to support things like sorting by `lat`, `lon`, or other fields, and postgres should make it easy to update fields to be foreign keys to get fast indexing.

### Why fastapi?
fastapi has better asynchronous support than flask so it should be a bit faster at scale. I also like the out-of-the-box docs it creates and the strong typing and built-in validation provided by pydantic.

## Questions
`api/tip`
- If our call to the task-satellite failed, do we want to add the entry to the db still?

`api/callback`
- Is there any extra validation we should do on the callback endpoint? The spec says `Returning a HTTP 200 / OK will acknowledge receipt of the callback. Any other response will tell the provider to retry later.`, but would we have to worry about cases where we wouldn't want them to try again? An example would be if we get a call to the callback endpoint with a `tipIdentifier` that somehow doesn't already exist in our table.
- What if we already had data from a previous callback to the same `tipIdentifier`? 

- Before we actually send the tip request, we want to make sure another tip hasn't been submitted **EXPIRATION DATE** within 30 minutes and within 10 nautical miles