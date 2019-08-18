# Redbrick Admin Exams

An attempt to collect the answers to all the Redbrick Admin Exams. This make it
easier for those in the future. Exams found at
https://redbrick.dcu.ie/help/exams

## Building exams

To build up to date exams from the source run `make` from the route directory.
Yaml docs will be read in from `src` directory and output to the `exam`
directory.

To setup dependencies you can run `make install`, **requires** python 3 and pip

## Format of the data

Rather then having all exams stored as markdown files for each year they are
stored as yaml broken down by section. This is to try to limit the repetition
that comes with question reuse.

- All files are stored in `src`, each file represents a section.
- Each file contains an array of questions.
- A Question has 3 fields, `question`, `answer`, and `years`.
  - `question` and `answer` are markdown strings.
  - `years` is an dictionary of years,
    - Each year is a `key` of the year, containing an array of strings to
      represent what exam the question was used in

### Example

````yaml
- question: >-
    Mailing lists are broken and we need to send the announce to all our users.
    Write a script to send the announce to our list of users, which is stored in
    a csv file, of `name,username,alt-mail` called `iShouldntHaveThis.csv`.
  answer: |-
    ```bash
    while IFS=, read -r col1 col2 col3
    do
        echo "$col2@redbrick.dcu.ie" >> emails.txt
    done < iShouldNotHaveThis.csv

    var=$(tr '\n', ',' < emails.txt)
    email=$(cat announce.txt)
    echo "Subject:Test
    From:branch@redbrick.dcu.ie

    $email" | sendmail -t $var
    ```
  years:
    2017:
      - AGM
      - EGM-1
    2018:
      - AGM
````

## Contributing

If you see any inconsistencies, wrong answers, missing information, or even some
spelling mistakes, don't be an asshole about it - fix it!

In relation to contributing, here's the guidelines:

1. This isn't the place to discuss what should or should not be on the admin
   exam. We literally just need to collect the answers to past iterations.

2. When it comes to making changes, just feel free to make a PR. It will be
   reviewed and changes might be requested. Ideally, it's not just myself that
   conducts PR review, but for now it is.

3. Bonus points if you keep every line within 80 char though this is not
   required.

If there's a significant amount of material contributed, say three or four years
worth of exams, I'd be happy to move this repository over to
[Redbrick's Github](https://github.com/redbrick). I don't mind if this little
project goes unfinished, but I don't intend to let be be unfinished on the
Redbrick Github, I hate that we've left a lot of half-hearted stuff there
already.
