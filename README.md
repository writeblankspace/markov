# Markov bot

A simple markov chain Discord bot with a ratio of 1.5:1.

For the purpose of this program, we will call the output of the markov chain (while it is being generated) a **Blagh**.

A Blagh:
- Must not be an empty string (what will the bot output?)
- Can contain any number of words, phrases and sentences
- May not follow grammar rules of any language
- Can be absolute nonsense

## Chain

Used in building Blaghs.

Where `n` is the position of the word to be added next.

| column | description |
| --- | --- |
| `word1` |  `n - 2` |
| `word2` | `n - 1` |
| `next` | `n` |
| `freq` | the frequency of this chain in training data |

- `word1` and `word2` may be `NULL`, so the first word in the Blagh will be `next`
- If `next` is `NULL`, the Blagh ends

> [!TIP] 
> 
> Take this example table for a 2:1 ratio:
> 
> | `word1` | `word2` | `next` | `freq` |
> | --- | --- | --- | --- |
> | `NULL` | `NULL` | the | 4 |
> | `NULL` | the | quick | 4 |
> | the | quick | brown | 3 |
> | the | quick | red | 1 |
> | lazy | dog | `NULL` | 4 |
> 
> When the current string is `"the quick"`, the word to be added is randomly chosen between `"brown"` and `"red"`.
> 
> Since `"brown"` is more frequent than `"red"`, however, it is more likely to be picked.
> 
> Thus, there is a 3/4 chance that we will get the string, `"the quick brown"`.

The bot uses a 1.5:1 ratio, meaning results matching both `word1` and `word2` will be weighted more than results matching only `word2`.

## Response

Used to start off a Blagh in reply to a message.

Usually, markov chains would consider a whole invoker message to come up with a response, but I decided to do it differently.

| column | description |
| --- | --- |
| `word1` | an important word from the invoker message |
| `word2` | another important word from the invoker message |
| `next` | the first two words of the response (or less, if the response ends in less than that) |
| `freq` | the frequency of this combination in training data |

An **important word**, in this program, is considered to be any of the following:
- A capitalied word
- A word used frequently in the message (>=4 characters)
- A long word

When no word in the invoker message matches the criteria, an important word may be any of the 3 longest words in the message.

Important words are ranked based on (in order of importance):
- Frequency in message
- Length
- Capitalization
- Position in message

> [!TIP]
> Take these lines from *Act 1, Scene 1* of Shakespeare's *A Midsummer Night's Dream*:
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
> The 7 most important words from Lysander's dialogue, in order, are:
> 1. how
> 2. chance
> 3. cheek
> 4. roses
> 5. there
> 6. love
> 7. why

We consider *combinations* of `word1` and `word2`, not *permutations*. The program checks for existing records of both permutations of the words.

### Extracting important words

There can only be up to 7 important words. Once we have 7 words, we stop adding new ones. These 7 words are each given points.

The capitalized words are first extracted from the text. These are usually either proper nouns or words put in ALL CAPS by the invoker — clearly important!
 
The most frequent words (>=4 characters) are then extracted, and given 1 point.

The longest words from the text are then extracted.

The list of 7 words is then sorted by points, then sub-sorted by length and position in the message. They are then put in lowercase.

### Training

Up to 5 records may be created or updated for each invoking message.

The important words are extracted, and added to the database.

> [!TIP]
> Let's continue using the excerpt from *A Midsummer Night's Dream*.
> 
> | `word1` | `word2` | `next` | `freq` |
> | --- | --- | --- | --- |
> | how | chance | Belike for | 1 |
> | how | cheek | Belike for | 1 |
> | how | roses | Belike for | 1 |
> | chance | cheek | Belike for | 1 |
> | chance | roses | Belike for | 1 |

### Responding

The important words are extracted from the invoking message.

The program will search for records containing the most important word or the 2nd most important word.

These are then given points based on:
- Whether the `word_` matches the most important word or the 2nd most important word
- Whether or not the other `word_` in the record matches any of the other important words
- The frequency of the response

The Blagh is started off with a random `next`, with the number of points given consideration.

## Todo

- [x] Ignore @mentions, @everyone and URLs
- [ ] Set status
- [ ] Use slash commands
- [x] Reduce ratio to 1.5:1
    - considers `word2` matches, not just `word1` AND `word2`
- [x] More efficient way of picking a random item based on weight
- [ ] Response
    - [ ] Important words
    - [ ] Training
    - [ ] Responding