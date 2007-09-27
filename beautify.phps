<?php
/*

JS Beautifier

(c) 2007, Einars "elfz" Lielmanis

http://elfz.laacz.lv/beautify/


You are free to use this in any way you want, in case you find this useful or working for you.

Usage: 
    require('beautify.php'); 
    js_beautify($js_source_text);

Intended to be used on the webpage, so it just prints htmlescaped pretty javascript.

You may wish to do some ob_start() and ob_get_contents() in your world. Or just rewrite.

Recent changes:

    2007-09-28 - slightly better handling of switch cases and lines not ending with semicolons
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
define('TK_WHITESPACE',    ++$n);
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




function js_beautify($js_source_text)
{
    global $lasttok, $lastword, $in, $ins, $indent;

    $lastword = '';


    // words which should always start on new line. 
    // simple hack for cases when lines aren't ending with semicolon.
    // feel free to tell me about the ones that need to be added. 
    $line_starters = explode(',', 'var,if,switch,for,while,break');


    // states showing if we are currently in expression (i.e. "if" case) - IN_EXPR, or in usual block (like, procedure), IN_BLOCK.
    // some formatting depends on that.
    $in       = IN_BLOCK;
    $ins      = array($in);

    $indent   = 0;

    $pos      = 0;

    $lasttok  = TK_EOF;

    while (true) {
        list($token_text, $token_type) = get_next_token($js_source_text, $pos);
        $token_text = htmlspecialchars($token_text);
        if ($token_type == TK_EOF) {
            break;
        }
        switch($token_type) {

        case TK_START_EXPR:

            in(IN_EXPR);
            if ($lasttok == TK_END_EXPR) {
                if ($token_text != '[') nl();
            } elseif ($lasttok != TK_WORD && $lasttok != TK_START_EXPR && $lasttok != TK_PUNCT) {
                echo ' ';
            } elseif ($lastword == 'if' || $lastword == 'for'  || $lastword == 'while') echo ' ';
            echo $token_text;
            break;

        case TK_END_EXPR:

            echo $token_text;
            in_pop();
            break;

        case TK_START_BLOCK:

            in(IN_BLOCK);
            if ($lasttok != TK_PUNCT) echo ' ';
            echo '{';
            indent();
            break;

        case TK_END_BLOCK:

            if ($lasttok == TK_END_EXPR) {
                nl();
                unindent();
            } elseif ($lasttok == TK_END_BLOCK) {
                unindent();
                nl();
            } elseif ($lasttok == TK_START_BLOCK) {
                // nothing
                unindent();
            } else {
                unindent();
                nl();
            }
            echo $token_text;
            in_pop();
            break;

        case TK_WORD:

            $prefix = 'NONE';
            if ($lasttok == TK_END_BLOCK) {
                if (strtolower($token_text) != 'else') {
                    $prefix = 'NL';
                } else {
                    $prefix = 'SPACE';
                    echo ' ';
                }
            } elseif ($lasttok == TK_END_COMMAND && $in == IN_BLOCK) {
                $prefix = 'NL';
            } elseif ($lasttok == TK_END_COMMAND && $in == IN_EXPR) {
                $prefix = 'SPACE';
            } elseif ($lasttok == TK_WORD) {
                $prefix = 'SPACE'; 
            } elseif ($lasttok == TK_START_BLOCK) {
                $prefix = 'NL';
            } elseif ($lasttok == TK_END_EXPR) {
                global $indent;
                $indent++;
                nl();
                $indent--;
            }

            if (in_array($token_text, $line_starters) or $prefix == 'NL') {
                nl();
            } elseif ($prefix == 'SPACE') {
                echo ' ';
            }
            echo $token_text;
            break;

        case TK_END_COMMAND:

            echo ";";
            break;

        case TK_STRING:

            if ($lasttok == TK_START_BLOCK) {
                nl();
            } elseif ($lasttok == TK_WORD) {
                echo ' ';
            }
            echo colorize($token_text, 'color:red');
            break;

        case TK_PUNCT:

            $start_delim = true;
            $end_delim   = true;
            if ($token_text == ',') {
                if ($in == IN_EXPR) {
                    echo ', ';
                } else {
                    echo ',';
                    nl();
                }
                break;

            } elseif ($lasttok == TK_PUNCT) {
                $start_delim = false;
                $end_delim = false;

            } elseif ($token_text == '.') {
                $start_delim = false;
                $end_delim   = false;

            } elseif ($token_text == ':') {
                $start_delim = false;

            } elseif ($lasttok == TK_WORD) {
            }
            if ($start_delim) echo ' ';
            echo $token_text;
            if ($end_delim) echo ' ';
            break;

        case TK_BLOCK_COMMENT:

            echo "\n";
            echo colorize($token_text, 'color:green');
            nl();
            break;

        case TK_COMMENT:

            if ($lasttok != TK_COMMENT) nl();
            echo colorize($token_text, 'color:green');
            nl();
            break;

        case TK_UNKNOWN:

            echo " $token_text ";
            break;
        }

        $lasttok  = $token_type;
        $lastword = strtolower($token_text);

    }
}




function nl()
{
    global $indent;
    echo "\n" . str_repeat('    ', $indent);
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



function get_next_token(&$text, &$pos)
{
    global $lasttok;
    global $whitespace, $wordchar, $punct;


    if (!$whitespace) $whitespace = make_array("\n\r\t ");
    if (!$wordchar)   $wordchar   = make_array('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_$');
    if (!$punct)      $punct      = make_array(".,=?:*&%^+-*<>!|");


    $max_len      = strlen($text);
    $num_newlines = 0;

    do {
        if ($pos >= $max_len) {
            return array('', TK_EOF);
        }

        $c = $text[$pos];
        $pos += 1;
        if ($c == "\r") {
            $num_newlines += 1;
        }
    } while (in_array($c, $whitespace));

    if ($num_newlines > 1) {
        // theoretically it should be js_beautify job to print something
        for ($i = 1 ; $i < $num_newlines; $i++) nl();
    }


    if (in_array($c, $wordchar)) {
        if ($pos < $max_len) {
            while (in_array($text[$pos], $wordchar)) {
                $c .= $text[$pos];
                $pos += 1;
                if ($pos == $max_len) break;
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
        if ($text[$pos] == '*') {
            $comment = '';
            $pos += 1;
            if ($pos < $max_len){
                while (!($text[$pos] == '*' && isset($text[$pos + 1]) && $text[$pos + 1] == '/') && $pos < $max_len) {
                    $comment .= $text[$pos];
                    $pos += 1;
                    if ($pos >= $max_len) break;
                }
            }
            $pos +=2;
            return array("/*$comment*/", TK_BLOCK_COMMENT);
        }
        // peek for comment // ...
        if ($text[$pos] == '/') {
            $comment = $c;
            while ($text[$pos] != "\x0d" && $text[$pos] != "\x0a") {
                $comment .= $text[$pos];
                $pos += 1;
                if ($pos >= $max_len) break;
            }
            $pos += 1;
            return array($comment, TK_COMMENT);
        }

    }

    if ($c == "'" || // string
        $c == '"' || // string
        ($c == '/' && ($lasttok == TK_START_EXPR || $lasttok == TK_PUNCT || $lasttok == TK_EOF || $lasttok == TK_END_COMMAND))) { // regexp
        $sep = $c;
        $c   = '';
        $esc = false;

        if ($pos < $max_len) {

            while ($esc || $text[$pos] != $sep) {
                $c .= $text[$pos];
                if (!$esc) {
                    $esc = $text[$pos] == '\\';
                } else {
                    $esc = false;
                }
                $pos += 1;
                if ($pos >= $max_len) break;
            }

        }

        $pos += 1;
        if ($lasttok == TK_END_COMMAND) {
            nl();
        }
        return array($sep . $c . $sep, TK_STRING);
    }

    if (in_array($c, $punct)) {
        if ($pos < $max_len) {
            while (in_array($text[$pos], $punct)) {
                $c .= $text[$pos];
                $pos += 1;
                if ($pos >= $max_len) break;
            }
        }
        return array($c, TK_PUNCT);
    }

    if ($c == '/') {
        return array($c, TK_PUNCT);
    }

    return array($c, TK_UNKNOWN);
}



function colorize($what, $style)
{
    return $what;
//    return sprintf('<span style="%s">%s</span>', $style, $what);
}

?>
