def _build_person_info(data_str):
    splits = data_str.split("\n\n\n")
    person_info = dict()
    for line in splits:
        tokens = filter(None, line.split("\n"))  # splits line and filters out any empty strings
        if len(tokens) > 0:
            key = tokens[0].rstrip(":")
            if key == "birth":
                person_info['birth'] = dict()
                _get_date_and_place(key, tokens, person_info)
            elif key == "death":
                person_info['death'] = dict()
                _get_date_and_place(key, tokens, person_info)
            elif key == "burial":
                person_info['burial'] = dict()
                _get_place(key, tokens, person_info)
            elif key == "residence":
                person_info['residence'] = dict()
                _get_date_and_place(key, tokens, person_info)
            elif key == "obituary":
                person_info['obituary'] = dict()
                _get_date_and_place(key, tokens, person_info)
            elif key == "marriage":
                person_info['marriage'] = dict()
                _get_date_and_place(key, tokens, person_info)
            else:
                person_info['unknown'] = dict()
                _process_unknown(key, tokens, person_info)
    return person_info


def _process_unknown(key, tokens, person_info):
    raise NotImplementedError
    pass


def _process_name(name_str):
    name_splits = name_str.split()
    fullname = name_str
    lastname = name_splits[-1]
    firstname = name_splits[0]
    midnames = " ".join(name_splits[1:-1])
    return fullname, lastname, firstname, midnames


def _process_data(data_str):
    person_info = _build_person_info(data_str)
    bdate=bplace=ddate=dplace=odate=oplace=mplace=mdate= 'NULL'

    if "birth" in person_info:
        if "date" in person_info["birth"]:
            bdate=person_info["birth"]["date"]
        if "place" in person_info["birth"]:
            bplace=person_info["birth"]["place"]
    if "death" in person_info:
        if "date" in person_info["death"]:
            ddate=person_info["death"]["date"]
        if "place" in person_info["death"]:
            dplace=person_info["death"]["place"]
    if "obituary" in person_info:
        if "date" in person_info["obituary"]:
            odate=person_info["obituary"]["date"]
        if "place" in person_info["obituary"]:
            oplace=person_info["obituary"]["place"]
    if "marriage" in person_info:
        if "date" in person_info["marriage"]:
            mdate=person_info["marriage"]["date"]
        if "place" in person_info["marriage"]:
            mplace=person_info["marriage"]["place"]

    return bdate,bplace,ddate,dplace,odate,oplace,mplace, mdate


def _get_date_and_place(key, tokens, person_info):
    date = ""
    place = ""
    if len(tokens) >= 2:  # we at least have event date
        date = tokens[1]
        person_info[key]["date"] = date
    if len(tokens) >= 3:  # we have event place too
        place = tokens[2]
        person_info[key]["place"] = place


def _get_place(key, tokens, person_info):
    place = tokens[1]
    person_info[key]["place"] = place


def build_add_person_query(person, db_env):
    bdate, bplace, ddate, dplace, obitdate, obitplace, mplace, mdate = _process_data(person['data'])
    fullname, lastname, firstname, midname = _process_name(person['name'])
    url = person['url']
    peeps = person['relationships']

    # apostrophes screw up the query: replace with doubles wherever found
    peeps = peeps.replace("'", "''")
    fullname = fullname.replace("'", "''")
    firstname = firstname.replace("'", "''")
    midname = midname.replace("'", "''")
    lastname = lastname.replace("'", "''")
    bplace = bplace.replace("'", "''")
    dplace = dplace.replace("'", "''")
    mplace = mplace.replace("'", "''")
    obitplace = obitplace.replace("'", "''")

    query = "INSERT INTO " + db_env + "people.people(" + \
            "fullname, " \
            "firstname, " \
            "lastname, " \
            "midname, " \
            "birthdate, " \
            "deathdate, " \
            "obitdate, " \
            "obitpaper, " \
            "url, " \
            "fake, " \
            "deathplace, " \
            "birthplace, " \
            "obitplace, " \
            "marriageplace, "\
            "marriagedate, " \
            "relationships)" \
            "values (" \
            "'" + fullname + "','" \
            + firstname + "','" \
            + lastname + "','" \
            + midname + "','" \
            + bdate + "','" \
            + ddate + "','" \
            + obitdate + "','" \
            + "None" + "','" \
            + url + "','" \
            + "True" + "','" \
            + dplace + "','" \
            + bplace + "','" \
            + obitplace + "','"\
            + mplace + "','"\
            + mdate + "',\'" \
            + peeps + "\');"
    return query
