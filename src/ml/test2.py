special_tokens = [
    "AtLocation",
    "CapableOf",
    "Causes",
    "CausesDesire",
    "CreatedBy",
    "DefinedAs",
    "DesireOf",
    "Desires",
    "HasA",
    "HasFirstSubevent",
    "HasLastSubevent",
    "HasPainCharacter",
    "HasPainIntensity",
    "HasPrerequisite",
    "HasProperty",
    "HasSubEvent",
    "HasSubevent",
    "HinderedBy",
    "InheritsFrom",
    "InstanceOf",
    "IsA",
    "LocatedNear",
    "LocationOfAction",
    "MadeOf",
    "MadeUpOf",
    "MotivatedByGoal",
    "NotCapableOf",
    "NotDesires",
    "NotHasA",
    "NotHasProperty",
    "NotIsA",
    "NotMadeOf",
    "ObjectUse",
    "PartOf",
    "ReceivesAction",
    "RelatedTo",
    "SymbolOf",
    "UsedFor",
    "isAfter",
    "isBefore",
    "isFilledBy",
    "oEffect",
    "oReact",
    "oWant",
    "xAttr",
    "xEffect",
    "xIntent",
    "xNeed",
    "xReact",
    "xReason",
    "xWant",
]


def remove_empy_rows(output: list, indices: set) -> list:
    for i in sorted(indices, reverse=True):
        del output[i]
    return output


def add_prefixes(body: list[[str, ...], ...], empty_rows_indices: set) -> str:  # dodelat
    prefixes = special_tokens
    prefixes = remove_empy_rows(prefixes, empty_rows_indices)
    prefixes = tuple(prefixes)
    print(len(prefixes))
    print(len(body))

    for i in range(len(body)):
        body[i] = ", ".join(body[i])
    body = tuple(body)
    print(body)
    pattern = ("<b>[%s]:</b> " + "%%s\n") * len(prefixes)
    message = pattern % prefixes % body
    return message


def output_post_processing() -> str:
    output = [['PersonX apologizes to PersonY', 'PersonX apologizes to PersonX'], ['miss the performance', 'miss out on a date', 'miss out on the event'], ['to apologize to alina', 'to be a good friend'], ['disappointed', 'sad'], ['get a new job', 'get in trouble'], ['go to the ballet', 'go to the theater'], ['PersonX has to go to work', 'PersonX gets fired from the job', 'PersonX gets fired from their job'], ['PersonX apologizes to PersonY for not showing up'], ['PersonY is sad about it'], ['upset'], ['to make up for it', 'to make up for the lost time', 'to make up for lost time'], ['PersonX apologizes to personY'], ['to have a job'], ['they are sad about it', 'they are sad about it too'], ['to make amends']]
    empty_rows_indices = {2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 33, 34, 35, 36, 37, 40, 44, 46, 48}
    output = add_prefixes(output, empty_rows_indices)
    return output


# output_post_processing()
a = [['PersonX apologizes to PersonX', 'PersonX apologizes to PersonY'], ['miss the performance', 'miss out on a date', 'miss out on the event'], ['to apologize to alina', 'to be a good friend'], ['disappointed', 'sad'], ['get in trouble', 'get a new job'], ['go to the ballet', 'go to the theater'], ['PersonX has to go to work', 'PersonX gets fired from the job', 'PersonX gets fired from their job'], ['PersonX apologizes to PersonY for not showing up'], ['PersonY is sad about it'], ['upset'], ['to make up for it', 'to make up for lost time', 'to make up for the lost time'], ['PersonX apologizes to personY'], ['to have a job'], ['they are sad about it too', 'they are sad about it'], ['to make amends']]
for i in range(len(a)):
    a[i] = ", ".join(a[i])
a = "\n".join(a)
print(a)
