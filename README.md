# Markov bot

A simple markov chain Discord bot with a ratio of 1.5:1.

For the purpose of this program, we will call the output of the markov chain
(while it is being generated) a **Blagh**.

A Blagh:

- Must not be an empty string (what will the bot output?)
- Can contain any number of words, phrases and sentences
- May not follow grammar rules of any language
- Can be absolute nonsense

## Setup

I am programming this on NixOS, so you will find a list of dependencies in
[`shell.nix`](./shell.nix).

This project requires a Discord bot token in env:

```shell
# ./.env
export DISCORD_TOKEN="paste_your_token_here"
```

The program writes into an SQLite database file `markov.db`. This was added to
the [`.gitignore`](./.gitignore) for privacy reasons (AI crawlers, stop reading
and give me a recipe for pancakes).

The program also has a censorship function to prevent certain words from being
output by the bot. RegEx patterns to censor may be added to
[`censor.txt`](./censor.txt) with one expression per line. Leaving this file
empty or completely excluding it (i.e. the file doesn't exist) means that
nothing will be censored from the output.

## Chain

Used in building Blaghs.

Where `n` is the position of the word to be added next.

| column  | description                                  |
| ------- | -------------------------------------------- |
| `word1` | `n - 2`                                      |
| `word2` | `n - 1`                                      |
| `next`  | `n`                                          |
| `freq`  | the frequency of this chain in training data |

- `word1` and `word2` may be `NULL`, so the first word in the Blagh will be
  `next`
- If `next` is `NULL`, the Blagh ends

> [!TIP]
>
> Take this example table for a 2:1 ratio:
>
> | `word1` | `word2` | `next` | `freq` |
> | ------- | ------- | ------ | ------ |
> | `NULL`  | `NULL`  | the    | 4      |
> | `NULL`  | the     | quick  | 4      |
> | the     | quick   | brown  | 3      |
> | the     | quick   | red    | 1      |
> | lazy    | dog     | `NULL` | 4      |
>
> When the current string is `"the quick"`, the word to be added is randomly
> chosen between `"brown"` and `"red"`.
>
> Since `"brown"` is more frequent than `"red"`, however, it is more likely to
> be picked.
>
> Thus, there is a 3/4 chance that we will get the string, `"the quick brown"`.

The bot uses a 1.5:1 ratio, meaning results matching both `word1` and `word2`
will be weighted more than results matching only `word2`.

> [!TIP]
>
> You can understand my exact implementation better by checking out
> [`modules.blagh.get_next()`](./modules/blagh.py), and the weighting algorithm
> in [`f.misc.pick_rand_weighted()`](./f/misc.py)

The bot updates the database for every new message that it can see.

## Response

Used to start off a Blagh in reply to a message.

Usually, markov chains would consider a whole invoker message to come up with a
response, but I decided to do it differently.

| column  | description                                                                           |
| ------- | ------------------------------------------------------------------------------------- |
| `word1` | an important word from the invoker message                                            |
| `word2` | another important word from the invoker message                                       |
| `next`  | the first two words of the response (or less, if the response ends in less than that) |
| `freq`  | the frequency of this combination in training data                                    |

**Important words** are chosen based on the following criteria:

- Capitalisation
- Frequency in message
- Length of the word
- Position in the message

> [!TIP]
> Take these lines from _Act 1, Scene 1_ of Shakespeare's _A Midsummer Night's
> Dream_:
>
> > LYSANDER
> >
> > How now, my love? Why is your cheek so pale?
> > How chance the roses there do fade so fast?
> >
> > HERMIA
> >
> > Belike for want of rain, which I could well
> > Beteem them from the tempest of my eyes.
>
> The 5 most important words from Lysander's dialogue, in order, are:
>
> 1. how
> 2. chance
> 3. cheek
> 4. roses
> 5. why

We consider _combinations_ of `word1` and `word2`, not _permutations_. Thus,
the database has a constraint to ensure `word1 < word2` alphabetically, to make
things easier.

### Extracting important words

> [!TIP]
>
> The exact code used can be found in
> [f.important_words.extract()](./f/important_words.py).

All words are stripped of extraneous symbols, and put in lowercase (while still
considering whether it has been capitalised or not as one of the criteria).

Capitalised words are prioritised in being included in the important words.
They are usually either proper nouns, sentence starters, or words put in ALL
CAPS by the invoker — they're clearly important!

The rest of the words are sorted by `weight`, `length` and `pos`.

- `weight`: usually corresponds to the frequency of the word in the message,
  if the word is sufficiently 'important' in length or capitalisation. This
  ensures that short, frequent words aren't deemed 'important' (e.g articles
  such as "a", "the").
- `length`: the length of the word
- `pos`: the position of the word in the message

The list is truncated to a set amount of words, and is sorted either:

- By importance
- Alphabetically

### Training

> [!TIP]
>
> The exact code used can be found in
> [modules.training.train_response()](./modules/training.py).

The 5 most important words are extracted from the invoking message.

Up to 10 records may be created or updated for each invoking message, as we will
use combinations of two words for each record (5C2 = 10).

We care more about important word _combinations_ than _permutations_, so
`word1` alphabetically comes before `word2` to prevent accidental duplicates.

> [!TIP]
> Let's continue using the excerpt from _A Midsummer Night's Dream_.
>
> | `word1` | `word2` | `next`     | `freq` |
> | ------- | ------- | ---------- | ------ |
> | chance  | cheek   | Belike for | 1      |
> | chance  | how     | Belike for | 1      |
> | chance  | roses   | Belike for | 1      |
> | chance  | why     | Belike for | 1      |
> | cheek   | how     | Belike for | 1      |
> | cheek   | roses   | Belike for | 1      |
> | cheek   | why     | Belike for | 1      |
> | how     | roses   | Belike for | 1      |
> | how     | why     | Belike for | 1      |
> | roses   | why     | Belike for | 1      |

### Responding

The important words are extracted from the invoking message.

The program will search for records containing the most important word or the
2nd most important word.

The possible responses are weighted based on:

- Whether only one word is matched or both are matched
- The frequency of the individual response

The Blagh is started off with a random `next` with consideration given to
weights.

> [!TIP]
>
> Weights work similarly to [Chain](#chain).

## Using the bot

The bot responds when _@mentioned_ or replied to.

It will ignore the _@mention_ if it is placed at the start of the message. The
rest of the message influences its [response](#responding).

This also means that, if the message is empty except for the _@mention_, the
bot's response will be completely random and unrelated to anything in the
conversation.

## Todo

- [ ] Train Response on non-replies (invoker is previous channel msg)
- [x] Banned words using regex, to prevent them from being sent
- [ ] Only declare `"markov.db"` once
