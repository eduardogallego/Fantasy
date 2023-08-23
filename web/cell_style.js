
function cellStyleValue(value, row, index) {
    return {
        classes: 'right scale-' + Math.min(Math.floor(value / 10), 9)
    }
}

function cellStylePoints(value, row, index) {
    extra = ''
    if (value !== null) {
        if (value < 0) {
            extra = ' scale-N';
        } else {
            extra = ' scale-' + Math.min(Math.round(value), 9);
        }
    }
    return {
        classes: 'right' + extra
    }
}

function cellStyleClause(value, row, index) {
    if (value === '1d' || value === '2d') {
        return {
            classes: 'right warning'
        }
    } else if (value.indexOf('h') > -1 || value.indexOf('m') > -1 || value.indexOf('s') > -1) {
        return {
            classes: 'right error'
        }
    } else {
        var scale = Math.min(Math.floor(value / 10), 9);
        return {
            classes: 'right scale-' + scale
        }
    }
}

function cellStyleWarnings(value, row, index) {
    extra = ''
    if (value !== null) {
        if (value === 1) {
            extra = ' warning';
        } else if (value > 1) {
            extra = ' error';
        }
    }
    return {
        classes: 'right' + extra
    }
}
