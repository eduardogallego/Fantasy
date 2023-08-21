
function percentFormatter(value, row) {
    return value + '%';
}

function positionFormatter(value, row) {
    var position = 'POR';
    if (value === 2) {
        position = 'DEF';
    } else if (value === 3) {
        position = 'CEN';
    } else if (value === 4) {
        position = 'DEL';
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

function statusFormatter(value, row) {
    var status = value;
    if (value === 'ok') {
        return '';
    } else if (value === 'doubtful') {
        status = 'UNK';
    } else if (value === 'injured') {
        status = 'INJ';
    } else if (value === 'out_of_league') {
        status = 'OUT';
    } else if (value === 'suspended') {
        status = 'SUS';
    }
    return '<span class="status status-' + status + '">' + status + '</span>';
}
