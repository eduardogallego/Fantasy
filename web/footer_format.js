
function footItemCountFormatter(data) {
    return data.length;
}

function footBuyValueFormatter(data) {
    var total = 0;
    data.forEach(function(data) {
        total = total + parseFloat(data.buy_value);
    });
    return total.toFixed(0);
}

function footSaleValueFormatter(data) {
    var total = 0;
    data.forEach(function(data) {
        total = total + parseFloat(data.sale_value);
    });
    return total.toFixed(0);
}

function footBenefitValueFormatter(data) {
    var total = 0;
    data.forEach(function(data) {
        total = total + parseFloat(data.benefit);
    });
    return total.toFixed(0);
}

function footPercBenefitFormatter(data) {
    var total_buy = 0;
    data.forEach(function(data) {
        total_buy = total_buy + parseFloat(data.buy_value);
    });
    var total_sale = 0;
    data.forEach(function(data) {
        total_sale = total_sale + parseFloat(data.sale_value);
    });
    return ((total_sale - total_buy) * 100 / total_buy).toFixed(0) + '%';
}

function footChange3dFormatter(data) {
    var total = 0;
    data.forEach(function(data) {
        total = total + parseFloat(data.change_3d);
    });
    return total.toFixed(1);
}

function footPerc3dFormatter(data) {
    var total_sale = 0;
    data.forEach(function(data) {
        total_sale = total_sale + parseFloat(data.sale_value);
    });
    var total_3d = 0;
    data.forEach(function(data) {
        total_3d = total_3d + parseFloat(data.change_3d);
    });
    return (total_3d * 100 / total_sale).toFixed(0) + '%';
}

function footMatchesFormatter(data) {
    var matches = 0;
    data.forEach(function(data) {
        if (data.matches > matches) {
            matches = data.matches;
        }
    });
    return matches;
}

function footAverageFormatter(data) {
    var average = 0;
    data.forEach(function(data) {
        average = average + parseFloat(data.average);
    });
    return average;
}

function footPointsFormatter(data) {
    var total = 0;
    data.forEach(function(data) {
        total = total + parseFloat(data.points);
    });
    return total;
}

function footPointsLstFormatter(data) {
    var total = 0;
    data.forEach(function(data) {
        total = total + parseFloat(data.lastSeasonPoints);
    });
    return total;
}

function footTotalFormatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.total != null) {
            total = total + data.total;
        }
    });
    return total;
}

function footJ1Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j1 != null) {
            total = total + data.j1;
        }
    });
    return total;
}

function footJ2Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j2 != null) {
            total = total + data.j2;
        }
    });
    return total;
}

function footJ3Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j3 != null) {
            total = total + data.j3;
        }
    });
    return total;
}

function footJ4Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j4 != null) {
            total = total + data.j4;
        }
    });
    return total;
}

function footJ5Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j5 != null) {
            total = total + data.j5;
        }
    });
    return total;
}

function footJ6Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j6 != null) {
            total = total + data.j6;
        }
    });
    return total;
}

function footJ7Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j7 != null) {
            total = total + data.j7;
        }
    });
    return total;
}

function footJ8Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j8 != null) {
            total = total + data.j8;
        }
    });
    return total;
}

function footJ9Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j9 != null) {
            total = total + data.j9;
        }
    });
    return total;
}

function footJ10Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j10 != null) {
            total = total + data.j10;
        }
    });
    return total;
}

function footJ11Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j11 != null) {
            total = total + data.j11;
        }
    });
    return total;
}

function footJ12Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j12 != null) {
            total = total + data.j12;
        }
    });
    return total;
}

function footJ13Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j13 != null) {
            total = total + data.j13;
        }
    });
    return total;
}

function footJ14Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j14 != null) {
            total = total + data.j14;
        }
    });
    return total;
}

function footJ15Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j15 != null) {
            total = total + data.j15;
        }
    });
    return total;
}

function footJ16Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j16 != null) {
            total = total + data.j16;
        }
    });
    return total;
}

function footJ17Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j17 != null) {
            total = total + data.j17;
        }
    });
    return total;
}

function footJ18Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j18 != null) {
            total = total + data.j18;
        }
    });
    return total;
}

function footJ19Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j19 != null) {
            total = total + data.j19;
        }
    });
    return total;
}

function footJ20Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j20 != null) {
            total = total + data.j20;
        }
    });
    return total;
}

function footJ21Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j21 != null) {
            total = total + data.j21;
        }
    });
    return total;
}

function footJ22Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j22 != null) {
            total = total + data.j22;
        }
    });
    return total;
}

function footJ23Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j23 != null) {
            total = total + data.j23;
        }
    });
    return total;
}

function footJ24Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j24 != null) {
            total = total + data.j24;
        }
    });
    return total;
}

function footJ25Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j25 != null) {
            total = total + data.j25;
        }
    });
    return total;
}

function footJ25Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j25 != null) {
            total = total + data.j25;
        }
    });
    return total;
}

function footJ26Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j26 != null) {
            total = total + data.j26;
        }
    });
    return total;
}

function footJ27Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j27 != null) {
            total = total + data.j27;
        }
    });
    return total;
}

function footJ28Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j28 != null) {
            total = total + data.j28;
        }
    });
    return total;
}

function footJ29Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j29 != null) {
            total = total + data.j29;
        }
    });
    return total;
}

function footJ30Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j30 != null) {
            total = total + data.j30;
        }
    });
    return total;
}

function footJ31Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j31 != null) {
            total = total + data.j31;
        }
    });
    return total;
}

function footJ32Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j32 != null) {
            total = total + data.j32;
        }
    });
    return total;
}

function footJ33Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j33 != null) {
            total = total + data.j33;
        }
    });
    return total;
}

function footJ34Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j34 != null) {
            total = total + data.j34;
        }
    });
    return total;
}

function footJ35Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j35 != null) {
            total = total + data.j35;
        }
    });
    return total;
}

function footJ36Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j36 != null) {
            total = total + data.j36;
        }
    });
    return total;
}

function footJ37Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j37 != null) {
            total = total + data.j37;
        }
    });
    return total;
}

function footJ38Formatter(data) {
    var total = 0;
    data.forEach(function(data) {
        if (data.j38 != null) {
            total = total + data.j38;
        }
    });
    return total;
}
