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

| SignWriting                                                                                                                                          | Translation    | Description                                                                                                                                                                                                                                                |
|------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ![FSW: M546x518S30007482x483S22f07525x467S15a2f516x482](assets/examples/hello.png)                                                                   | Hello          | With your dominant open hand, fingers together and pointing up, place your fingertips near the right side of your forehead, palm angled away from your body. Move your hand forward (away from your body) in a straight path.                              |
| ![FSW: M531x539S2ff00482x482S26500517x507S33e00482x482S15a00494x512](assets/examples/thank-you.png)                                                  | Thank You      | With your dominant open hand, fingers together and pointing up, touch your fingertips to your lips, palm toward your body. Move your hand forward and slightly downward, palm toward the ceiling.                                                          |
| ![FSW: M517x527S15a37494x496S20500483x516S1f702490x490S22a00493x473](assets/examples/help.png)                                                       | Help (him/her) | Hold your non-dominant open hand flat in front of your torso, palm toward the ceiling. Place your dominant fist with thumb pointing up on that palm. Move both hands upward together.                                                                      |
| ![FSW: M516x513S13f10487x498S22114484x487](assets/examples/no-hand.png)                                                                              | No             | With your dominant hand, extend your index and middle fingers and extend your thumb, other fingers closed, palm toward your sideways. Bring the index and middle fingertips to touch the thumb twice with quick closing movements.                         |
| ![FSW: M518x524S30122482x476S30c00482x489](assets/examples/no-face.png)                                                                              | No             | Shake your head left and right while furrowing your eyebrows.                                                                                                                                                                                              |
| ![FSW: M511x520S1f701490x481S21100495x506](assets/examples/sorry.png)                                                                                | Sorry          | Form a fist with your dominant hand, palm toward your body. Rub the fist on your chest in a small clockwise circle repeatedly.                                                                                                                             |
| ![FSW: M535x542S1060a477x458S10621494x458S20800495x472S10629468x517S10602494x517S20800489x532S2d205502x485S2d211465x484](assets/examples/friend.png) | Friend         | With both hands, extend your index fingers, other fingers closed. Hook the two index fingers together in front of your chest. Alternate which index finger is on top with small switching movements.                                                       |
| ![FSW: M530x518S20500470x500S20305503x482S3770b488x496S37713487x496S20500520x499S20303474x483](assets/examples/love.png)                             | Love           | Form fists with both hands, palms toward your body. Cross your forearms over your chest so each fist rests near the opposite shoulder.                                                                                                                     |
| ![FSW: M522x525S11541498x491S11549479x498S20600489x476](assets/examples/name.png)                                                                    | Name           | With both hands, extend your index and middle fingers, other fingers closed, palms sideways. Place the middle-finger side of your dominant hand against the index-finger side of your non-dominant hand. Tap this side contact twice with small movements. |

## Conventions

All descriptions follow the conventions defined in [`CONVENTIONS.md`](signwriting_description/CONVENTIONS.md),
covering viewpoint, handshape naming, palm orientation, contact geometry, movement verbs, and more.

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

| SignWriting                                                                                                                                          | Translation    | Description                                                                                                                                                                                                                                                                                                                                                                                     |
|------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ![FSW: M546x518S30007482x483S22f07525x467S15a2f516x482](assets/examples/hello.png)                                                                   | Hello          | Place your non-dominant flat hand near the right side of your head, palm facing outward. Move your hand upward and downward twice in a straight path.                                                                                                                                                                                                                                           |
| ![FSW: M531x539S2ff00482x482S26500517x507S33e00482x482S15a00494x512](assets/examples/thank-you.png)                                                  | Thank You      | With your dominant hand flat, palm facing your body, place it under your chin. Move your hand upward slightly while maintaining a smile.                                                                                                                                                                                                                                                        |
| ![FSW: M517x527S15a37494x496S20500483x516S1f702490x490S22a00493x473](assets/examples/help.png)                                                       | Help (him/her) | With your dominant hand, form a fist with the thumb extended, palm facing your body. Place the thumb on your chest. Move your hand upward in a small straight path.                                                                                                                                                                                                                             |
| ![FSW: M516x513S13f10487x498S22114484x487](assets/examples/no-hand.png)                                                                              | No             | With your dominant hand, extend your index and middle fingers along with your thumb, palm facing sideways. Move your hand up and down in a large hinge motion.                                                                                                                                                                                                                                  |
| ![FSW: M518x524S30122482x476S30c00482x489](assets/examples/no-face.png)                                                                              | No             | Move your head slightly forward and back in a straight path while lowering your eyebrows.                                                                                                                                                                                                                                                                                                       |
| ![FSW: M511x520S1f701490x481S21100495x506](assets/examples/sorry.png)                                                                                | Sorry          | With your dominant hand, form a fist with the thumb extended, palm facing your body. Rub the thumb side of your fist in a small circular motion.                                                                                                                                                                                                                                                |
| ![FSW: M535x542S1060a477x458S10621494x458S20800495x472S10629468x517S10602494x517S20800489x532S2d205502x485S2d211465x484](assets/examples/friend.png) | Friend         | With both hands, form fists with bent index fingers. Position your non-dominant hand palm facing your body and your dominant hand palm facing outward. Bring the index fingers together in a grasping motion, then rotate both hands in a circular motion, hitting the floor plane. Repeat this motion with the non-dominant hand palm facing outward and the dominant hand palm facing inward. |
| ![FSW: M530x518S20500470x500S20305503x482S3770b488x496S37713487x496S20500520x499S20303474x483](assets/examples/love.png)                             | Love           | With both hands in fists, palms facing inward, cross your forearms in front of your chest. Tap the fists together lightly, alternating which fist is on top.                                                                                                                                                                                                                                    |
| ![FSW: M522x525S11541498x491S11549479x498S20600489x476](assets/examples/name.png)                                                                    | Name           | With both hands, extend your index and middle fingers together, other fingers closed. Position your hands so the fingertips touch each other repeatedly in front of your chest, palms facing sideways.                                                                                                                                                                                          |

## Evaluation

We use BLEU, chrF2, and an LLM-as-judge score to compare the hand-written descriptions to the ones outputted by ChatGPT using
[`signwriting_description/evaluation.py`](signwriting_description/evaluation.py).
The judge score (0–100) uses GPT-5.2 to annotate MQM-style errors aligned with [CONVENTIONS.md](signwriting_description/CONVENTIONS.md),
penalizing critical (-15), major (-10), and minor (-5) errors from a base of 100.

| Model | BLEU | chrF2 | Judge |
|-------|------|-------|-------|
| gpt-4.1-2025-04-14.md | 16.95 | 49.75 | 48.9 |
| gpt-5-2025-08-07.md | 18.03 | 50.39 | 43.9 |
| gpt-5.2-2025-12-11.md | 16.99 | 44.54 | 49.4 |

To recreate the evaluation files, run:

```shell
MODELS=(
    "gpt-4.1-2025-04-14"
    "gpt-5-2025-08-07"
    "gpt-5.2-2025-12-11"
)
for model in "${MODELS[@]}"; do
    output_file="signwriting_description/results/$model.md"
    if [ ! -f "$output_file" ]; then
        python -u -m signwriting_description.gpt_description --model="$model" | tee "$output_file"
    fi
done
```

### Custom Model

Ideally, we would like to use a model that is trained on SignWriting descriptions.
We can generate a dataset using ChatGPT, and then fine-tune a model on this dataset.

## Dockerized Web Server

```shell
docker build --tag signwriting-description .

docker run --rm -p 9873:8080 \
  -e PORT=8080 \
  -e OPENAI_API_KEY=your_openai_key \
  -e DISK_CACHE_DIR=/mnt/cache \
  -v $(pwd)/cache:/mnt/cache \
  signwriting-description

curl http://localhost:9873/?fsw=M546x518S30007482x483S22f07525x467S15a2f516x482
```
