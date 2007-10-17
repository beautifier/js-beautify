<?php // $Id$

/*

JS Beautifier

(c) 2007, Einars "elfz" Lielmanis

http://elfz.laacz.lv/beautify/


You are free to use this in any way you want, in case you find this useful or working for you.

Usage: 
    require('beautify.php'); 
    echo js_beautify($js_source_text);

As of 2007-09-28, it returns normal usable text. Remember to htmlescape if printing from webpage.

Recent changes:

    2007-10-17 - various minor improvements thanks to me starting writing tests even for this little crapsticle
    2007-09-28 - better handling of switch cases and lines not ending with semicolons
                 function returns just a proper text, instead of printing or htmlescaping input
                 utf-8 support (not in the variable names, though it will look ok, probably)
    2007-05-26 - regular expression appearing on the start of line, fixed
    2007-05-18 - error about uninitialized string offset in the end of the script fixed
    2007-03-13 - a little cleanup for the public
    2007-02-08 - created this stuff

*/

error_reporting(E_ALL);
ini_set('display_errors', 'on');


$n = 1;
define('IN_EXPR',          ++$n);
define('IN_BLOCK',         ++$n);


define('TK_UNKNOWN',       ++$n);
define('TK_WORD',          ++$n);
define('TK_START_EXPR',    ++$n);
define('TK_END_EXPR',      ++$n);
define('TK_START_BLOCK',   ++$n);
define('TK_END_BLOCK',     ++$n);
define('TK_END_COMMAND',   ++$n);
define('TK_EOF',           ++$n);
define('TK_STRING',        ++$n);

define('TK_BLOCK_COMMENT', ++$n);
define('TK_COMMENT',       ++$n);

define('TK_PUNCT',         ++$n);

// internal flags
define('PRINT_NONE',       ++$n);
define('PRINT_SPACE',      ++$n);
define('PRINT_NL',         ++$n);


function js_beautify($js_source_text, $tab_size = 4)
{
    global $output, $token_text, $last_type, $in, $ins, $indent, $tab_string;

    global $input, $input_length;

    $tab_string = str_repeat(' ', $tab_size); 

    $input = $js_source_text;
    $input_length = strlen($input);

    $last_word = ''; // last TK_WORD passed
    $last_type  = TK_EOF; // last token type
    $output = '';

    // words which should always start on new line. 
    // simple hack for cases when lines aren't ending with semicolon.
    // feel free to tell me about the ones that need to be added. 
    $line_starters = explode(',', 'throw,return,var,if,switch,case,default,for,while,break');

    // states showing if we are currently in expression (i.e. "if" case) - IN_EXPR, or in usual block (like, procedure), IN_BLOCK.
    // some formatting depends on that.
    $in       = IN_BLOCK;
    $ins      = array($in);


    $indent   = 0;

    $pos      = 0; // parser position


    while (true) {
        list($token_text, $token_type) = get_next_token($pos);
        if ($token_type == TK_EOF) {
            break;
        }
        switch($token_type) {

        case TK_START_EXPR:

            in(IN_EXPR);
            if ($last_type == TK_END_EXPR or $last_type == TK_START_EXPR) {
                // do nothing on (( and )( and ][ and ]( .. 
            } elseif ($last_type != TK_WORD and $last_type != TK_PUNCT) {
                space();
            } elseif (in_array($last_word, $line_starters)) { 
                space();
            }
            token();
            break;

        case TK_END_EXPR:

            token();
            in_pop();
            break;

        case TK_START_BLOCK:

            in(IN_BLOCK);
            if ($last_type != TK_PUNCT and $last_type != TK_START_EXPR) {
                space();
            }
            token();
            indent();
            break;

        case TK_END_BLOCK:

            if ($last_type == TK_END_EXPR) {
                nl();
                unindent();
            } elseif ($last_type == TK_END_BLOCK) {
                unindent();
                nl();
            } elseif ($last_type == TK_START_BLOCK) {
                // nothing
                unindent();
            } else {
                unindent();
                nl();
            }
            token();
            in_pop();
            break;

        case TK_WORD:
            
            $prefix = PRINT_NONE;
            if ($last_type == TK_END_BLOCK) {
                if (!in_array(strtolower($token_text), array('else', 'catch', 'finally'))) {
                    $prefix = PRINT_NL;
                } else {
                    $prefix = PRINT_SPACE;
                    space();
                }
            } elseif ($last_type == TK_END_COMMAND && $in == IN_BLOCK) {
                $prefix = PRINT_NL;
            } elseif ($last_type == TK_END_COMMAND && $in == IN_EXPR) {
                $prefix = PRINT_SPACE;
            } elseif ($last_type == TK_WORD) {
                $prefix = PRINT_SPACE; 
            } elseif ($last_type == TK_START_BLOCK) {
                $prefix = PRINT_NL;
            } elseif ($last_type == TK_END_EXPR) {
                $indent++;
                nl();
                $indent--;
            }

            if (in_array($token_text, $line_starters) or $prefix == PRINT_NL) {
                if ($last_type != TK_END_EXPR) {
                    if ($last_type != TK_START_EXPR or $token_text != 'var') { // no need to force newline on 'var': for (var x = 0...)
                        nl();
                    }
                }
            } elseif ($prefix == PRINT_SPACE) {
                space();              
            }
            token();
            $last_word = strtolower($token_text);
            break;

        case TK_END_COMMAND:

            token();
            break;

        case TK_STRING:

            if ($last_type == TK_START_BLOCK) {
                nl();
            } elseif ($last_type == TK_WORD) {
                space();
            }
            token();
            break;

        case TK_PUNCT:
            $start_delim = true;
            $end_delim   = true;
            if ($token_text == ',') {
                if ($in == IN_EXPR) {
                    token();
                    space();
                } else {
                    token();
                    nl();
                }
                break;
            } elseif ($token_text == '--' or $token_text == '++') { // unary operators special case
                $start_delim = false;
                $end_delim = false;
            } elseif ($token_text == '!' and $last_type == TK_START_EXPR) {
                // special case handling: if (!a)
                $start_delim = false;
                $end_delim = false;
            } elseif ($last_type == TK_PUNCT) {
                $start_delim = false;
                $end_delim = false;
            } elseif ($last_type == TK_END_EXPR) {
                $start_delim = true;
                $end_delim = true;
            } elseif ($token_text == '.') {
                // decimal digits or object.property
                $start_delim = false;
                $end_delim   = false;

            } elseif ($token_text == ':') {
                // zz: xx
                // can't differentiate ternary op, so for now it's a ? b: c; without space before colon
                $start_delim = false;
            } elseif ($last_type == TK_WORD) {
            }
            if ($start_delim) {
                space();
            }

            token();
            
            if ($end_delim) {
                space();
            }
            break;

        case TK_BLOCK_COMMENT:

            nl();
            token();
            nl();
            break;

        case TK_COMMENT:

            if ($last_type != TK_COMMENT) {
                nl();
            }
            token();
            nl();
            break;

        case TK_UNKNOWN:
            token();
            break;
        }

        $last_type  = $token_type;
    }

    return $output;
}




function nl($ignore_repeated = true)
{
    global $indent, $output, $tab_string;

    if ($output == '') return; // no newline on start of file

    if ($ignore_repeated) {
        if ($output and substr($output, -1) == "\n") return;
    }

    $output .= "\n" . str_repeat($tab_string, $indent);
}


function space()
{
    global $output;
    if ($output and substr($output, -1) != ' ') { // prevent occassional duplicate space
        $output .= ' ';
    }
}


function token()
{
    global $token_text, $output;
    $output .= $token_text;
}

function indent()
{
    global $indent;
    $indent ++;
}


function unindent()
{
    global $indent;
    if ($indent) {
        $indent --;
    }
}



function in($where)
{
    global $ins, $in;
    array_push($ins, $in);
    $in = $where;
}


function in_pop()
{
    global $ins, $in;
    $in = array_pop($ins);
}



function make_array($str)
{
    $res = array();
    for ($i = 0; $i < strlen($str); $i++) {
        $res[] = $str[$i];
    }
    return $res;
}



function get_next_token(&$pos)
{
    global $last_type;
    global $whitespace, $wordchar, $punct;
    global $input, $input_length;


    if (!$whitespace) $whitespace = make_array("\n\r\t ");
    if (!$wordchar)   $wordchar   = make_array('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_$');
    if (!$punct)      $punct  = explode(' ', '+ - * / % & ++ -- = += -= *= /= %= == === != > < >= <= >> << >>> <<< >>= <<= &&  | || ! !! , : ?'); 

    $num_newlines = 0;

    do {
        if ($pos >= $input_length) {
            return array('', TK_EOF);
        }
        $c = $input[$pos];
        $pos += 1;
        if ($c == "\n") {
            $num_newlines += 1;
        }
    } while (in_array($c, $whitespace));

    if ($num_newlines > 1) {
        // theoretically it should be js_beautify job to print something
        for ($i = 1 ; $i <= $num_newlines; $i++) nl(false);
    }


    if (in_array($c, $wordchar)) {
        if ($pos < $input_length) {
            while (in_array($input[$pos], $wordchar)) {
                $c .= $input[$pos];
                $pos += 1;
                if ($pos == $input_length) break;
            }
        }
        return array($c, TK_WORD);
    }

    if ($c == '(' || $c == '[') {
        return array($c, TK_START_EXPR);
    }

    if ($c == ')' || $c == ']') {
        return array($c, TK_END_EXPR);
    }

    if ($c == '{') {
        return array($c, TK_START_BLOCK);
    }

    if ($c == '}') {
        return array($c, TK_END_BLOCK);
    }

    if ($c == ';') {
        return array($c, TK_END_COMMAND);
    }

    if ($c == '/') {
        // peek for comment /* ... */
        if ($input[$pos] == '*') {
            $comment = '';
            $pos += 1;
            if ($pos < $input_length){
                while (!($input[$pos] == '*' && isset($input[$pos + 1]) && $input[$pos + 1] == '/') && $pos < $input_length) {
                    $comment .= $input[$pos];
                    $pos += 1;
                    if ($pos >= $input_length) break;
                }
            }
            $pos +=2;
            return array("/*$comment*/", TK_BLOCK_COMMENT);
        }
        // peek for comment // ...
        if ($input[$pos] == '/') {
            $comment = $c;
            while ($input[$pos] != "\x0d" && $input[$pos] != "\x0a") {
                $comment .= $input[$pos];
                $pos += 1;
                if ($pos >= $input_length) break;
            }
            $pos += 1;
            return array($comment, TK_COMMENT);
        }

    }

    if ($c == "'" || // string
        $c == '"' || // string
        ($c == '/' && ($last_type == TK_START_EXPR || $last_type == TK_PUNCT || $last_type == TK_EOF || $last_type == TK_END_COMMAND))) { // regexp
        $sep = $c;
        $c   = '';
        $esc = false;

        if ($pos < $input_length) {

            while ($esc || $input[$pos] != $sep) {
                $c .= $input[$pos];
                if (!$esc) {
                    $esc = $input[$pos] == '\\';
                } else {
                    $esc = false;
                }
                $pos += 1;
                if ($pos >= $input_length) break;
            }

        }

        $pos += 1;
        if ($last_type == TK_END_COMMAND) {
            nl();
        }
        return array($sep . $c . $sep, TK_STRING);
    }

    if (in_array($c, $punct)) {
        while (in_array($c . $input[$pos], $punct)) {
            $c .= $input[$pos];
            $pos += 1;
            if ($pos >= $input_length) break;
        }
        return array($c, TK_PUNCT);
    }

    return array($c, TK_UNKNOWN);
}

?>
