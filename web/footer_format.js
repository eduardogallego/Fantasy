
function footItemCountFormatter(data) {
    return data.length;
}

function footMaxFormatter(data) {
    var max = 0;
    var column = this.field;
    data.forEach(function(data) {
        eval('var value = data.' + column + ';');
        if (value > max) {
            max = data.matches;
        }
    });
    return max;
}

function footSumFormatter(data) {
    var sum = 0;
    var column = this.field;
    data.forEach(function(data) {
        eval('var value = data.' + column + ';');
        if (value != null) {
            sum = sum + value;
        }
    });
    return sum;
}

function footSum0DFormatter(data) {
    var sum = 0;
    var column = this.field;
    data.forEach(function(data) {
        eval('var value = data.' + column + ';');
        if (value != null) {
            sum = sum + parseFloat(value);
        }
    });
    return sum.toFixed(0);
}

function footSum0SoldFormatter(data) {
    var sum = 0;
    var column = this.field;
    data.forEach(function(data) {
        if (data.sale_value != null) {
            eval('var value = data.' + column + ';');
            if (value != null) {
                sum = sum + parseFloat(value);
            }
        }
    });
    return sum.toFixed(0);
}

function footSum1DFormatter(data) {
    var sum = 0;
    var column = this.field;
    data.forEach(function(data) {
        eval('var value = data.' + column + ';');
        if (value != null) {
            sum = sum + parseFloat(value);
        }
    });
    return sum.toFixed(1);
}

function footSumTopFormatter(data) {
    var sum = 0;
    var column = this.field;
    data.forEach(function(data) {
        eval('var value = data.' + column + ';');
        if (value != null && data.tag > 0) {
            sum = sum + parseFloat(value);
        }
    });
    return sum.toFixed(0);
}

function footPercBenefitFormatter(data) {
    var total_buy = 0;
    var total_sale = 0;
    data.forEach(function(data) {
        total_buy = total_buy + parseFloat(data.buy_value);
        total_sale = total_sale + parseFloat(data.sale_value);
    });
    return ((total_sale - total_buy) * 100 / total_buy).toFixed(0) + '%';
}

function footPercBenefitClauseFormatter(data) {
    var total_buy = 0;
    var total_sale = 0;
    var total_clause = 0;
    data.forEach(function(data) {
        if (data.sale_value != null) {
            total_buy = total_buy + parseFloat(data.buy_value);
            total_sale = total_sale + parseFloat(data.sale_value);
            total_clause = total_clause + parseFloat(data.clause_update);
        }
    });
    return ((total_sale - total_buy - total_clause) * 100 / (total_buy + total_clause)).toFixed(0) + '%';
}

function footPerc3dFormatter(data) {
    var total_sale = 0;
    var total_3d = 0;
    data.forEach(function(data) {
        total_sale = total_sale + parseFloat(data.sale_value);
        total_3d = total_3d + parseFloat(data.change_3d);
    });
    return (total_3d * 100 / total_sale).toFixed(0) + '%';
}
