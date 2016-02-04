//--------//
// Inputs //
//--------//

var operator_position = {
    sanity: [
        'var res = a + b - c / d * e % f;',
        'var res = g & h | i ^ j;',
        'var res = (k && l || m) ? n : o;',
        'var res = p >> q << r >>> s;',
        'var res = t === u !== v != w == x >= y <= z > aa < ab;',
        'ac + -ad'
    ],
    comprehensive: [
        'var res = a + b',
        '- c /',
        'd  *     e',
        '%',
        'f;',
        '   var res = g & h',
        '| i ^',
        'j;',
        'var res = (k &&',
        'l',
        '|| m) ?',
        'n',
        ': o',
        ';',
        'var res = p',
        '>> q <<',
        'r',
        '>>> s;',
        'var res',
        '  = t',
        '',
        ' === u !== v',
        ' !=',
        'w',
        '== x >=',
        'y <= z > aa <',
        'ab;',
        'ac +',
        '-ad'
    ],
    colon_special_case: [
        'var a = {',
        '    b',
        ': bval,',
        '    c:',
        'cval',
        '    ,d: dval',
        '};',
        'var e = f ? g',
        ': h;',
        'var i = j ? k :',
        'l;'
    ],
    catch_all: [
        'var d = 1;',
        'if (a === b',
        '    && c) {',
        '    d = (c * everything',
        '            / something_else) %',
        '        b;',
        '    e',
        '        += d;',
        '',
        '} else if (!(complex && simple) ||',
        '    (emotion && emotion.name === "happy")) {',
        '    cryTearsOfJoy(many ||',
        '        anOcean',
        '        || aRiver);',
        '}'
    ]
};


//---------//
// Exports //
//---------//

module.exports = {
    operator_position: operator_position
};