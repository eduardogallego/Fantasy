
function cellStyleValue(value, row, index) {
    var scale = Math.min(Math.floor(value / 10), 9);
    return {
        classes: 'right scale-' + scale
    }
}

function clauseStyleValue(value, row, index) {
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
