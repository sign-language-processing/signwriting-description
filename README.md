# SignWriting Description

Based on [sign/translate#130](https://github.com/sign/translate/issues/130).

The written representation of signed languages is challenging due to the complexities of various writing systems.
SignWriting, though beneficial, demand specialized linguistic expertise for effective use.

This repository aims to provide a solution for the automatic description of SignWriting in spoken languages.
This solution can be used for teaching SignWriting to new learners, fine-tuning translation models,
or zero-shot inference on motion generation models.

## Examples

In English, we make a few examples of SignWriting with translation and description.
While the translation is language specific, the description is language agnostic.
(This was generated using [`signwriting_description/few_shots/readme.py`](signwriting_description/few_shots/readme.py))

| SignWriting                                                                                                                                          | Translation    | Description                                                                                                                                                                  |
|------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ![FSW: M546x518S30007482x483S22f07525x467S15a2f516x482](assets/examples/hello.png)                                                                   | Hello          | With your dominant hand open, touch your forehead and move your hand away, palm facing out.                                                                                  |
| ![FSW: M531x539S2ff00482x482S26500517x507S33e00482x482S15a00494x512](assets/examples/thank-you.png)                                                  | Thank You      | Touch your dominant open hand to your lips, then move your hand forward, palm up.                                                                                            |
| ![FSW: M526x532S15a37484x501S20500473x521S1f702480x495S26627504x468](assets/examples/help.png)                                                       | Help (him/her) | Place your dominant hand's fist (thumb up) on the palm of your open non-dominant hand. Move both hands upward together.                                                      |
| ![FSW: M516x513S13f10487x498S22114484x487](assets/examples/no-hand.png)                                                                              | No             | With your dominant hand, extend your index and middle fingers while keeping your other fingers tucked in. Tap these fingers against your thumb.                              |
| ![FSW: M518x524S30122482x476S30c00482x489](assets/examples/no-face.png)                                                                              | No             | Shake your head horizontally while forrowing your eyebrows.                                                                                                                  |
| ![FSW: M511x520S1f701490x481S21100495x506](assets/examples/sorry.png)                                                                                | Sorry          | Form a fist with your dominant hand, palm facing in. Circle it over your heart.                                                                                              |
| ![FSW: M535x542S1060a477x458S10621494x458S20800495x472S10629468x517S10602494x517S20800489x532S2d205502x485S2d211465x484](assets/examples/friend.png) | Friend         | Link the index fingers of both hands together, alternating their positions.                                                                                                  |
| ![FSW: M530x518S20500470x500S20305503x482S3770b488x496S37713487x496S20500520x499S20303474x483](assets/examples/love.png)                             | Love           | Cross your arms over your chest as if giving yourself a hug, with your hands forming fists.                                                                                  |
| ![FSW: M522x525S11541498x491S11549479x498S20600489x476](assets/examples/name.png)                                                                    | Name           | With your dominant hand, extend your index and middle fingers. Tap these fingers twice onto the extended index finger of your non-dominant hand, which is held horizontally. |

## Methodology

### Naive Description

We start with a naive description of the SignWriting image, by describing each symbol in the image.
We use the [symbol names](signwriting_description/symbols.json) to generate a
non-natural description ([naive_description](signwriting_description/naive_description.py)).

For example, the "Hello" sign above would be described as:

```txt
SIGNWRITING HEAD RIM (Head Rims) top right of the face at x: 482, y: 483
SIGNWRITING MOVEMENT-WALLPLANE DOUBLE STRAIGHT (Double Straight Movement, Wall Plane) dominant hand rotated 45 degrees clockwise at x: 525, y: 467
SIGNWRITING HAND-FLAT (Flat) left hand palm facing outwards, parallel to the wall rotated 45 degrees clockwise at x: 516, y: 482
```

This description is not natural, but it is a good start to name the symbols and their positions.

### GPT Description

To generate a more natural description, we use ChatGPT over the naive description, and SignWriting image.
We feed in all of the above examples for few-shot prediction.

For example, if we exclude each sign from the few-shots, we predict:

| SignWriting                                                                                                                                          | Translation    | Description                                                                                                                                  |
|------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| ![FSW: M546x518S30007482x483S22f07525x467S15a2f516x482](assets/examples/hello.png)                                                                   | Hello          | Place your non-dominant flat hand near the side of your head, palm facing out. Move it outward in two straight motions.                      |
| ![FSW: M531x539S2ff00482x482S26500517x507S33e00482x482S15a00494x512](assets/examples/thank-you.png)                                                  | Thank You      | With a smile, place your flat dominant hand under your chin and move it slightly upward.                                                     |
| ![FSW: M526x532S15a37484x501S20500473x521S1f702480x495S26627504x468](assets/examples/help.png)                                                       | Help (him/her) | Start with your dominant hand open, palm up. Touch your thumb to your palm, then move your hand forward and slightly upward.                 |
| ![FSW: M516x513S13f10487x498S22114484x487](assets/examples/no-hand.png)                                                                              | No             | With your dominant hand, form a fist with the index, middle fingers, and thumb extended. Move your hand up and down in a large hinge motion. |
| ![FSW: M518x524S30122482x476S30c00482x489](assets/examples/no-face.png)                                                                              | No             | Move your head straight forward while furrowing your eyebrows downward.                                                                      |
| ![FSW: M511x520S1f701490x481S21100495x506](assets/examples/sorry.png)                                                                                | Sorry          | With your dominant hand in a fist, rub your thumb in a circular motion against your palm.                                                    |
| ![FSW: M535x542S1060a477x458S10621494x458S20800495x472S10629468x517S10602494x517S20800489x532S2d205502x485S2d211465x484](assets/examples/friend.png) | Friend         | With both hands, extend and bend your index fingers. Move them in a grasping motion, rotating your wrists slightly as if turning a knob.     |
| ![FSW: M530x518S20500470x500S20305503x482S3770b488x496S37713487x496S20500520x499S20303474x483](assets/examples/love.png)                             | Love           | Cross your arms in front of you, forming fists with both hands. Tap your fists together once.                                                |
| ![FSW: M522x525S11541498x491S11549479x498S20600489x476](assets/examples/name.png)                                                                    | Name           | Bring both hands together with index and middle fingers extended and touching, then tap them together repeatedly.                            |

## Evaluation

We use BLEU and chrF to compare the hand-written descriptions to the ones outputted by ChatGPT using
[`signwriting_description/evaluation.py`](signwriting_description/evaluation.py), resulting in:

| Model                        | BLEU  | chrF2 |
|------------------------------|-------|-------|
| GPT-4 Vision (deprecated).md | 14.42 | 37.03 |
| GPT-4 Omni (unknown).md      | 10.76 | 42.41 |
| GPT-4 Omni 2024-05-13.md     | 12.35 | 40.81 |
| GPT-4 Omni 2024-08-06.md     | 9.53  | 39.60 |

### Custom Model

Ideally, we would like to use a model that is trained on SignWriting descriptions.
We can generate a dataset using ChatGPT, and then fine-tune a model on this dataset.