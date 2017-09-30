from collections import defaultdict
from datetime import timezone

from app.db import CONNECTION as db
from app.auth import requires_auth

from flask import Flask, render_template, request, make_response
app = Flask(__name__)

def getValue(data, key):
    values = list(filter(lambda d: d['name'] == key, data))
    return values[0]['value'] if len(values) > 0 else None

def getBusRiders(query={}):
    return db.users.find({
        'applied': True,
        'accepted': True,
        'applicationBranch': {
            '$in': [
                'Participant',
                'Mentor'
            ]
        },
        **query
    }, {
        'attending': True,
        'applicationBranch': True,
        'applicationData': True,
        'confirmationBranch': True,
        'confirmationSubmitTime': True,
        'confirmationDeadlines': True
    })

def getCurrentDeadline(db, branch):
    branch = db.questionbranchconfigs.find_one({
        'name': branch
    })
    return branch['settings']['close']

def getValue(values, name, key='value'):
    pairs = list(filter(lambda pair: pair['name']==name, values))
    return pairs[0][key] if len(pairs) > 0 else None

@app.route('/')
@requires_auth
def dashboard():
    branchName = "Don't Need Reimbursement"
    currentDeadline = getCurrentDeadline(db, branchName).replace(tzinfo=timezone.utc).astimezone(tz=None)

    deadlines = defaultdict(lambda: [])
    for user in getBusRiders():
        if user['attending'] is True and user['confirmationBranch'] != branchName:
            continue
        close = getValue(user['confirmationDeadlines'], branchName, 'close') if 'confirmationDeadlines' in user else None
        if close is not None:
            deadlines[close].append(user)
        else:
            deadlines[currentDeadline].append(user)

    isGT = lambda u: (getValue(u['applicationData'], 'school') if u['applicationBranch'] == 'Participant' else getValue(u['applicationData'], 'school-if-student')) == 'Georgia Institute of Technology'
    deadlines = sorted(map(lambda pair: {
        'time': pair[0].replace(tzinfo=timezone.utc).astimezone(tz=None),
        'total': len(pair[1]),
        'attending': len(list(filter(lambda u: u['attending'] is True, pair[1]))),
        'GTtotal': len(list(filter(isGT, pair[1]))),
        'GTattending': len(list(filter(lambda u: isGT(u) and u['attending'], pair[1])))
    }, deadlines.items()), key=lambda d: d['time'])

    return render_template('dashboard.html', currentDeadline=currentDeadline, deadlines=list(deadlines))
