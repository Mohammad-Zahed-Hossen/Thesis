# Codebook

Code from the output and the two problems only. Don't look at the key or the other coder's sheet.

attempted_problem: which problem does the working operate on, ignoring any opening description?
    image | text | both | neither. Use "both" if it mixes facts from the two problems.
    Judge what it works on, not whether the arithmetic is right.
refused: does the model decline to give a solution, with no solving attempted afterwards?
    yes | no. "Cannot determine if they agree. However, I can solve..." is "no".
verdict: what does the output say about how the image and text relate? Use the part before solving.
    conflict   | says they disagree, contradict, or present different problems
    agree      | says they agree or are consistent
    cannot_determine | says it can't tell whether they agree
    no_relation | says there is no agreement or contradiction between them
    no_info    | says they give no information, without any of the above
    none       | says nothing about how they relate
stated_reliable: which source does the output call more reliable?
    image | text | undetermined (raises reliability, names neither) | absent (doesn't raise it)

Valid codes are lower case, exactly as written above.
