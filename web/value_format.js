
function percentFormatter(value, row) {
    if (value == null) {
        return '';
    } else {
        return value + '%';
    }
}

function positionFormatter(value, row) {
    var position = 'P';
    if (value === 2) {
        position = 'D';
    } else if (value === 3) {
        position = 'C';
    } else if (value === 4) {
        position = 'A';
    }
    return '<span class="position pos-' + value + '">' + position + '</span>';
}

function teamFormatter(value, row) {
    if (value === 'atletico-de-madrid') {
        value = 'ATM';
    } else if (value === 'athletic-club') {
        value = 'ATH';
    } else if (value === 'cadiz-cf') {
        value = 'CAD';
    } else if (value === 'c-a-osasuna') {
        value = 'OSA';
    } else if (value === 'd-alaves') {
        value = 'ALA';
    } else if (value === 'fc-barcelona') {
        value = 'BAR';
    } else if (value === 'getafe-cf') {
        value = 'GET';
    } else if (value === 'granada-cf') {
        value = 'GRA';
    } else if (value === 'girona-fc') {
        value = 'GIR';
    } else if (value === 'rayo-vallecano') {
        value = 'RAY';
    } else if (value === 'rc-celta') {
        value = 'CEL';
    } else if (value === 'rcd-mallorca') {
        value = 'MLL';
    } else if (value === 'real-betis') {
        value = 'BET';
    } else if (value === 'real-madrid') {
        value = 'RMA';
    } else if (value === 'real-sociedad') {
        value = 'RSO';
    } else if (value === 'sevilla-fc') {
        value = 'SEV';
    } else if (value === 'valencia-cf') {
        value = 'VAL';
    } else if (value === 'villarreal-cf') {
        value = 'VIL';
    } else if (value === 'ud-almeria') {
        value = 'ALM';
    } else if (value === 'ud-las-palmas') {
        value = 'LPA';
    }
    return '<span class="team team-' + value + '">' + value + '</span>';
}

function ownerFormatter(value, row) {
    if (value === null) {
        return '';
    }
    if (value === 'Jesus_Ciudad') {
        value = 'JES';
    } else if (value === 'Edu') {
        value = 'EDU';
    } else if (value === 'liebana_team') {
        value = 'LIE';
    } else if (value === 'Moncho RoMa') {
        value = 'RAM';
    } else if (value === 'Nicojeda') {
        value = 'NIC';
    } else if (value === 'Cocolan FC') {
        value = 'COC';
    } else if (value === 'sporting cocolan') {
        value = 'SPO';
    }
    return '<span class="owner own-' + value + '">' + value + '</span>';
}

function playerFormatter(value, row) {
    var icons = '';
    if (row.tag != 0) {
        var color = 'others';
        if (row.tag == 1) {
            color = 'gold';
        } else if (row.tag == 2) {
            color = 'silver'
        } else if (row.tag == 3) {
            color = 'bronze'
        }
        icons = '<i class="bi bi-star-fill ' + color + '"></i> ';
    }
    var status = '';
    if (row.status != 'ok') {
        if (row.status === 'doubtful') {
            status = '<i class="bi bi-question-circle-fill"></i>';
        } else if (row.status === 'injured') {
            status = '<i class="bi bi-bandaid-fill"></i>';
        } else if (row.status === 'out_of_league') {
            status = '<i class="bi bi-forward-fill"></i>';
        } else if (row.status === 'suspended') {
            status = '<i class="bi bi-file-fill"></i>';
        }
    }
    return value + ' ' + icons + status
}
