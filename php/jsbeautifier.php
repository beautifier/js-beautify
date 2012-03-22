<?php
/*
Naming conventions kept over from python code.

Originally written by Einar Lielmanis et al.,
Conversion to PHP by Kaspars Foigts, laacz@laacz.lv,
MIT licence, enjoy.

Performance is dreadful. If you want to improve stuff, do so.

Just include this into your PHP script, and use it away. Example:

<?php
require('path/to/jsbeautifier.php');

# Beautify string
$result = js_beautify('your javascript string');

# Beautify file
$result = js_beautify(file_get_contents('some_file.js'));

# You may specify some options:
$opts = new BeautifierOptions();
$opts->indent_size = 2;
$result = js_beautify('some javascript', $opts);
?>

*/


define('TK_EOF',             0);
define('TK_START_EXPR',      1);
define('TK_END_EXPR',        2);
define('TK_START_BLOCK',     3);
define('TK_END_BLOCK',       4);
define('TK_WORD',            5);
define('TK_SEMICOLON',       6);
define('TK_STRING',          7);
define('TK_EQUALS',          8);
define('TK_OPERATOR',        9);
define('TK_BLOCK_COMMENT',  10);
define('TK_INLINE_COMMENT', 11);
define('TK_COMMENT',        12);
define('TK_UNKNOWN',        13);


class BeautifierOptions {
    var $indent_size = 4;
    var $indent_char = ' ';
    var $indent_with_tabs = false;
    var $preserve_newlines = true;
    var $max_preserve_newlines = 10;
    var $jslint_happy = false;
    var $brace_style = 'collapse';
    var $keep_array_indentation = false;
    var $keep_function_indentation = false;
    var $eval_code = false;
}

class BeautifierFlags {
    var $previous_mode = 'BLOCK';
    var $mode;
    var $var_line = false;
    var $var_line_tainted = false;
    var $var_line_reindented = false;
    var $in_html_comment = false;
    var $if_line = false;
    var $in_case = false;
    var $eat_next_space = false;
    var $indentation_baseline = -1;
    var $indentation_level = 0;
    var $ternary_depth = 0;

    function __construct($mode) {
    	$this->mode = $mode;
    }
}	


function js_beautify($string, $options = null) {
	$beautifier = new JSBeautifier();
	return $beautifier->beautify($string, $options);
}

class JSBeautifier {

	var $options;
	
	function __construct($options = null) {
		$this->options = $options ?: new BeautifierOptions();
		$this->blank_state();
	}

	function blank_state() {
        $this->flags = new BeautifierFlags('BLOCK');
        $this->flag_store = Array();
        $this->wanted_newline = false;
        $this->just_added_newline = false;
        $this->do_block_just_closed = false;

        $this->indent_string = $this->options->indent_with_tabs ? "\t" : str_repeat($this->options->indent_char, $this->options->indent_size);

        $this->preindent_string = '';
        $this->last_word = '';              # last TK_WORD seen
        $this->last_type = TK_START_EXPR; # last token type
        $this->last_text = '';              # last token text
        $this->last_last_text = '';         # pre-last token text

        $this->input = null;
        $this->output = Array();            # formatted javascript gets built here

        $this->whitespace = Array("\n", "\r", "\t", " ");
        $this->wordchar = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_$';
        $this->digits = '0123456789';
        $this->punct = '+ - * / % & ++ -- = += -= *= /= %= == === != !== > < >= <= >> << >>> >>>= >>= <<= && &= | || ! !! , : ? ^ ^= |= ::';
        $this->punct .= ' <?= <? ?> <%= <% %>';
        $this->punct = explode(' ', $this->punct);

        $this->line_starters = explode(',', 'continue,try,throw,return,var,if,switch,case,default,for,while,break,function');
        $this->set_mode('BLOCK');

        $this->parser_pos = 0;
	}

	function set_mode($mode) {
        $prev = new BeautifierFlags('BLOCK');

        if (isset($this->flags)) {
        	$this->flag_store[] = $this->flags;
        	$prev = $this->flags;
        }

        $this->flags = new BeautifierFlags($mode);

        if (isset($this->flag_store) && (count($this->flag_store) == 1)) {
        	$this->flags->indentation_level = 0;
        } else {
        	$this->flags->indentation_level = $prev->indentation_level;
        	if ($prev->var_line && $prev->var_line_reindented) {
        		$this->flags->indentation_level++;
        	}
        }
        $this->flags->previous_mode = $prev->mode;

	}

	function beautify($string, $options = null) {
		if ($options) $this->options = $options;
		
		if (!in_array($this->options->brace_style, Array('expand', 'collapse', 'end-expand'))) {
			throw new Wxception('opts.brace_style must be "expand", "collapse" or "end-expand".');
		}

		$this->blank_state();

		while ($string && strpos(" \t", $string[0]) !== false) {
			$this->preindent_string .= $string[0];
			$string = substr($string, 1);
		}

		# TODO: Implement unpackers
		# self.input = self.unpack(s, opts.eval_code)
		$this->input = $string;

		$this->parser_pos = 0;
		$handlers = Array(
            TK_START_EXPR     => 'handle_start_expr',
            TK_END_EXPR       => 'handle_end_expr',
            TK_START_BLOCK    => 'handle_start_block',
            TK_END_BLOCK      => 'handle_end_block',
            TK_WORD           => 'handle_word',
            TK_SEMICOLON      => 'handle_semicolon',
            TK_STRING         => 'handle_string',
            TK_EQUALS         => 'handle_equals',
            TK_OPERATOR       => 'handle_operator',
            TK_BLOCK_COMMENT  => 'handle_block_comment',
            TK_INLINE_COMMENT => 'handle_inline_comment',
            TK_COMMENT        => 'handle_comment',
            TK_UNKNOWN        => 'handle_unknown',
		);

		while (true) {
			list($token_text, $token_type) = $this->get_next_token();
			if ($token_type === TK_EOF) {
				break;
			}
            $token_type_str = 'N/A';
            foreach (get_defined_constants() as $k=>$v) {
                if (substr($k, 0, 3) == 'TK_' && $v == $token_type) {
                    $token_type_str = $k;
                    break;
                }
            }
			//echo $token_type_str . "\t" . $token_text . "\n";
            $this->$handlers[$token_type]($token_text);
            $this->last_last_text = $this->last_text;
			$this->last_type = $token_type;
			$this->last_text = $token_text;
		}

		$sweet_code = $this->preindent_string . preg_replace("/[\n ]+$/", '', join('', $this->output));
		return $sweet_code;
	}

    function handle_equals($token_text) {
        if ($this->flags->var_line) {
            # just got an '=' in a var-line, different line breaking rules will apply
            $this->flags->var_line_tainted = true;
        }
        $this->append(' ');
        $this->append($token_text);
        $this->append(' ');
    }

    function handle_semicolon($token_text) {
        $this->append($token_text);
        $this->flags->var_line = false;
        $this->flags->var_line_reindented = false;
        if ($this->flags->mode == 'OBJECT') {
            # OBJECT mode is weird and doesn't get reset too well.
            $this->flags->mode = 'BLOCK';
        }
    }

	function trim_output($eat_newlines = false) {
		while (count($this->output) && ($this->output[count($this->output)-1] == ' ' ||
										$this->output[count($this->output)-1] == $this->indent_string ||
										$this->output[count($this->output)-1] == $this->preindent_string ||
										($eat_newlines && (strpos("\n\r", $this->output[count($this->output)-1]) !== false)))) {
			array_pop($this->output);
		}
	}


	function get_next_token() {

		$this->n_newlines = 0;
		if ($this->parser_pos >= strlen($this->input)) {
			return array('', TK_EOF);
		}

		$this->wanted_newline = false;
		$c = $this->input[$this->parser_pos];
		$this->parser_pos++;

		$keep_whitespace = $this->options->keep_array_indentation && $this->is_array($this->flags->mode);

		if ($keep_whitespace) {
            # slight mess to allow nice preservation of array indentation and reindent that correctly
            # first time when we get to the arrays:
            # var a = [
            # ....'something'
            # we make note of whitespace_count = 4 into flags.indentation_baseline
            # so we know that 4 whitespaces in original source match indent_level of reindented source
            #
            # and afterwards, when we get to
            #    'something,
            # .......'something else'
            # we know that this should be indented to indent_level + (7 - indentation_baseline) spaces

            $whitespace_count = 0;
            while (in_array($c, $this->whitespace) !== false) {
				switch ($c) {
            		case "\n":
            			$this->trim_output();
            			$this->output[] = "\n";
            			$this->just_added_newline = true;
            			$whitespace_count = 0;
            			break;
            		case "\t":
            			$whitespace_count += 4;
            			break;
            		case "\r":
            			break;
            		default:
            			$whitespace_count++;
            			break;
            	}
            	if ($this->parser_pos >= strlen($this->input)) {
                    return array('', TK_EOF);
            	}

            	$c = $this->input[$this->parser_pos];
            	$this->parser_pos++;
            }

            if ($this->flags->indentation_baseline == -1) {
            	$this->flags->indentation_baseline = $whitespace_count;
            }

            if ($this->just_added_newline) {
            	for ($i = 0; $i <= $this->flags->indentation_level; $i++) {
            		$this->output[] = $this->indent_string;
            	}

            	if ($this->flags->indentation_baseline != -1) {
            		for ($i = 0; $i < $whitespace_count - $this->flags->indentation_baseline; $i++) {
            			$this->output[] = ' ';
            		}
            	}
            }

		} else { # not keep_whitespace
			while (in_array($c, $this->whitespace)) {
				if ($c == "\n") {
					if ($this->options->max_preserve_newlines == 0 || ($this->options->max_preserve_newlines > $this->n_newlines)) {
						$this->n_newlines++;
					}
				}
				if ($this->parser_pos >= strlen($this->input)) {
					return Array('', TK_EOF);
				}

				$c = $this->input[$this->parser_pos];
				$this->parser_pos++;
			}

			if ($this->options->preserve_newlines && $this->n_newlines > 1) {
				for ($i = 0; $i < $this->n_newlines; $i++) {
					$this->append_newline($i == 0);
					$this->just_added_newline = true;
				}
			}
			
			$this->wanted_newline = $this->n_newlines > 0;
		}

		if (strpos($this->wordchar, $c) !== false) {
            if ($this->parser_pos < strlen($this->input)) {
				while (strpos($this->wordchar, $this->input[$this->parser_pos]) !== false) {
					$c .= $this->input[$this->parser_pos];
					$this->parser_pos++;
					if ($this->parser_pos == strlen($this->input)) {
						break;
					} 
				}
			}

			# small and surprisingly unugly hack for 1E-10 representation
			if (($this->parser_pos != strlen($this->input)) && 
			    (strpos('+-', $this->input[$this->parser_pos]) !== false) &&
			    preg_match('/^[0-9]+[Ee]$/', $c)) {
			    $sign = $this->input[$this->parser_pos];
			    $this->parser_pos++;
			    $t = $this->get_next_token();
			    $c .= $sign . $t[0];
			    return Array($c, TK_WORD);
			}

			if ($c == 'in') { # in is an operator, need to hack
				return Array($c, TK_OPERATOR);
			}

			if ($this->wanted_newline &&
				($this->last_type != TK_OPERATOR) &&
				($this->last_type != TK_EQUALS) &&
				!$this->flags->if_line &&
				($this->options->preserve_newlines || ($this->last_text != 'var'))) {
				$this->append_newline();
			}
            return Array($c, TK_WORD);
		}

		if (strpos('([', $c) !== false) {
			return Array($c, TK_START_EXPR);
		}

		if (strpos(')]', $c) !== false) {
			return Array($c, TK_END_EXPR);
		}

		if ($c == '{') {
			return Array($c, TK_START_BLOCK);
		}

		if ($c == '}') {
			return Array($c, TK_END_BLOCK);
		}

		if ($c == ';') {
			return Array($c, TK_SEMICOLON);
		}

		if ($c == '/') {
			$comment = '';
			$inline_comment = True;
			$comment_mode = TK_INLINE_COMMENT;

			if ($this->input[$this->parser_pos] == '*') { # peek /* .. */ comment
				$this->parser_pos++;

				if ($this->parser_pos < strlen($this->input)) {
					while (!(($this->input[$this->parser_pos] == '*') &&
                             ($this->parser_pos + 1 < strlen($this->input)) &&
                             ($this->input[$this->parser_pos + 1] == '/')) &&
                            ($this->parser_pos < strlen($this->input))) {
                        $c = $this->input[$this->parser_pos];
                        $comment .= $c;
                        if (strpos("\r\n", $c) !== false) {
                            $comment_mode = TK_BLOCK_COMMENT;
                        }
                        $this->parser_pos ++;
                        if ($this->parser_pos >= strlen($this->input)) {
                            break;
                        }
                    }
				}
                $this->parser_pos += 2;
                return Array('/*' . $comment . '*/', $comment_mode);
			}
            if ($this->input[$this->parser_pos] == '/') { # peek // comment
                $comment = $c;
                while (strpos("\r\n", $this->input[$this->parser_pos]) === false) {
                    $comment .= $this->input[$this->parser_pos];
                    $this->parser_pos++;
                    if ($this->parser_pos >= strlen($this->input)) {
                        break;
                    }
                }
                $this->parser_pos ++;
                if ($this->wanted_newline) {
                    $this->append_newline();
                }
                return Array($comment, TK_COMMENT);
            }
		}

        if (($c == "'") || ($c == '"') || 
            ($c == '/' && (($this->last_type == TK_WORD && in_array($this->last_text, Array('return', 'do'))) ||
                           (in_array($this->last_type, Array(TK_COMMENT, TK_START_EXPR, TK_START_BLOCK, TK_END_BLOCK, TK_OPERATOR,
                                                             TK_EQUALS, TK_EOF, TK_SEMICOLON)))))) {
                                        
            $sep = $c;
            $esc = false;
            $resulting_string = $c;
            $in_char_class = false;

            if ($this->parser_pos < strlen($this->input)) {
                if ($sep == '/') {
                    # handle regexp
                    $in_char_class = false;
                    while ($esc || $in_char_class || $this->input[$this->parser_pos] != $sep) {
                        $resulting_string .= $this->input[$this->parser_pos];
                        if (!$esc) {
                            $esc = $this->input[$this->parser_pos] == '\\';
                            if ($this->input[$this->parser_pos] == '[') {
                                $in_char_class = true;
                            } elseif($this->input[$this->parser_pos] == ']') {
                                $in_char_class = false;
                            }
                        } else {
                            $esc = false;
                        }
                        $this->parser_pos++;
                        if ($this->parser_pos >= strlen($this->input)) {
                            # incomplete regex when end-of-file reached
                            # bail out with what has received so far
                            return Array($resulting_string, TK_STRING);
                        }
                    }
                } else {
                    # handle string
                    while ($esc || $this->input[$this->parser_pos] != $sep) {
                        $resulting_string .= $this->input[$this->parser_pos];
                        if (!$esc) {
                            $esc = $this->input[$this->parser_pos] == '\\';
                        } else {
                            $esc = false;
                        }
                        $this->parser_pos++;
                        if ($this->parser_pos >= strlen($this->input)) {
                            # incomplete string when end-of-file reached
                            # bail out with what has received so far
                            return Array($resulting_string, TK_STRING);
                        }
                    }
                }
            }
            $this->parser_pos++;
            $resulting_string .= $sep;

            if ($sep == '/') {
                # regexps may have modifiers /regexp/MOD, so fetch those too
                while ($this->parser_pos < strlen($this->input) && strpos($this->wordchar, $this->input[$this->parser_pos]) !== false) {
                    $resulting_string .= $this->input[$this->parser_pos];
                    $this->parser_pos++;
                }
            }

            return Array($resulting_string, TK_STRING);
        }

        if ($c == '#') {
            
            # she-bang
            if (count($this->output) == 0 && strlen($this->input) > 1 && $this->input[$this->parser_pos] == '!') {
                $resulting_string = $c;
                while ($this->parser_pos < strlen($this->input) && $c != "\n") {
                    $c = $this->input[$this->parser_pos];
                    $resulting_string .= $c;
                    $this->parser_pos++;
                }
                $this->output[] = trim($resulting_string) . "\n";
                $this->append_newline();
                return $this->get_next_token();
            }

            # Spidermonkey-specific sharp variables for circular references
            # https://developer.mozilla.org/En/Sharp_variables_in_JavaScript
            # http://mxr.mozilla.org/mozilla-central/source/js/src/jsscan.cpp around line 1935
            $sharp = '#';
            if ($this->parser_pos < strlen($this->input) && strpos($this->digits, $this->input[$this->parser_pos]) !== false) {
                while (true) {
                    $c = $this->input[$this->parser_pos];
                    $sharp .= $c;
                    $this->parser_pos++;
                    if ($this->parser_pos >= strlen($this->input) || $c == '#' || $c == '=') {
                        break;
                    }
                }
            }
            if ($c == '#' || $this->parser_pos >= strlen($this->input)) {
                ;
            } elseif ($this->input[$this->parser_pos] == '[' && $this->input[$this->parser_pos+1] == ']') {
                $sharp .= '[]';
                $this->parser_pos += 2;
            } elseif ($this->input[$this->parser_pos] == '{' && $this->input[$this->parser_pos+1] == '}') {
                $sharp .= '{}';
                $this->parser_pos += 2;
            }
            return Array($sharp, TK_WORD);
        }

        if ($c == '<' && substr($this->input, $this->parser_pos - 1, 4) == '<!--') {
            $this->parser_pos += 3;
            $this->flags->in_html_comment = true;
            return Array('<!--', TK_COMMENT);
        }

        if ($c == '-' && $this->flags->in_html_comment && substr($this->input, $this->parser_pos - 1, 3) == '-->') {
            $this->flags->in_html_comment = false;
            $this->parser_pos += 2;
            if ($this->wanted_newline) {
                $this->append_newline();
            }
            return Array('-->', TK_COMMENT);
        }

        if (in_array($c, $this->punct)) {
            while ($this->parser_pos < strlen($this->input) && in_array($c . $this->input[$this->parser_pos], $this->punct)) {
                $c .= $this->input[$this->parser_pos];
                $this->parser_pos++;
                if ($this->parser_pos >= strlen($this->input)) {
                    break;
                }
            }
            if ($c == '=') {
                return Array($c, TK_EQUALS);
            } else {
                return Array($c, TK_OPERATOR);
            }
        }

        return Array($c, TK_UNKNOWN);

	}

    function handle_start_expr($token_text) {
        if ($token_text == '[') {
            if ($this->last_type == TK_WORD || $this->last_text == ')') {
                if (in_array($this->last_text, $this->line_starters)) {
                    $this->append(' ');
                }
                $this->set_mode('(EXPRESSION)');
                $this->append($token_text);
                return;
            }

            if (in_array($this->flags->mode, Array('[EXPRESSION]', '[INDENTED-EXPRESSION]'))) {
                if ($this->last_last_text == ']' && $this->last_text == ',') {
                    # ], [ goers to a new line
                    if ($this->flags->mode == '[EXPRESSION]') {
                        $this->flags->mode = '[INDENTED-EXPRESSION]';
                        if (!$this->options->keep_array_indentation) {
                            $this->indent();
                        }
                    }
                    $this->set_mode('[EXPRESSION]');
                    if (!$this->options->keep_array_indentation) {
                        $this->append_newline();
                    }
                } elseif ($this->last_text == '[') {
                    if ($this->flags->mode == '[EXPRESSION]') {
                        $this->flags->mode = '[INDENTED-EXPRESSION]';
                        if (!$this->options->keep_array_indentation) {
                            $this->indent();
                        }
                    }
                    $this->set_mode('[EXPRESSION]');

                    if (!$this->options->keep_array_indentation) {
                        $this->append_newline();
                    }
                } else {
                    $this->set_mode('[EXPRESSION]');
                }
            } else {
                $this->set_mode('[EXPRESSION]');
            }
        } else {
            $this->set_mode('(EXPRESSION)');
        }

        if ($this->last_text == ';' || $this->last_type == TK_START_BLOCK) {
            $this->append_newline();
        } elseif (in_array($this->last_type, Array(TK_END_EXPR, TK_START_EXPR, TK_END_BLOCK)) || $this->last_text == '.') {
            # do nothing on (( and )( and ][ and ]( and .(
        } elseif (!in_array($this->last_type, Array(TK_WORD, TK_OPERATOR))) {
            $this->append(' ');
        } elseif ($this->last_word == 'function' || $this->last_word == 'typeof') {
            # function() vs function (), typeof() vs typeof ()
            if ($this->options->jslint_happy) {
                $this->append(' ');
            }
        } elseif (in_array($this->last_text, $this->line_starters) || $this->last_text == 'catch') {
            $this->append(' ');
        }

        $this->append($token_text);
    }

    function handle_end_expr($token_text) {
        if ($token_text == ']') {
            if ($this->options->keep_array_indentation) {
                if ($this->last_text == '}') {
                    $this->remove_indent();
                    $this->append($token_text);
                    $this->restore_mode();
                    return;
                }
            } else {
                if ($this->flags->mode == '[INDENTED-EXPRESSION]') {
                    if ($this->last_text == ']') {
                        $this->restore_mode();
                        $this->append_newline();
                        $this->append($token_text);
                        return;
                    }
                }
            }
        }
        $this->restore_mode();
        $this->append($token_text);
    }

    function handle_start_block($token_text) {
        if ($this->last_word == 'do') {
            $this->set_mode('DO_BLOCK');
        } else {
            $this->set_mode('BLOCK');
        }

        if ($this->options->brace_style == 'expand') {
            if ($this->last_type != TK_OPERATOR) {
                if (in_array($this->last_text, Array('return', '='))) {
                    $this->append(' ');
                } else {
                    $this->append_newline(true);
                }
            }

            $this->append($token_text);
            $this->indent();
        } else {
            if (!in_array($this->last_type, Array(TK_OPERATOR, TK_START_EXPR))) {
                if ($this->last_type == TK_START_BLOCK) {
                    $this->append_newline();
                } else {
                    $this->append(' ');
                }
            } else {
                # if TK_OPERATOR or TK_START_EXPR
                if ($this->is_array($this->flags->previous_mode) && $this->last_text == ',') {
                    if ($this->last_last_text == '}') {
                        
                        $this->append(' ');
                    } else {
                        $this->append_newline();
                    }
                }
            }
            $this->indent();
            $this->append($token_text);
        }
    }

    function handle_end_block($token_text) {
        $this->restore_mode();
        if ($this->options->brace_style == 'expand') {
            if ($this->last_text != '{') {
                $this->append_newline();
            }
        } else {
            if ($this->last_type == TK_START_BLOCK) {
                if ($this->just_added_newline) {
                    $this->remove_indent();
                } else {
                    # {}
                    $this->trim_output();
                }
            } else {
                if ($this->is_array($this->flags->mode) && $this->options->keep_array_indentation) {
                    $this->options->keep_array_indentation = false;
                    $this->append_newline();
                    $this->options->keep_array_indentation = true;
                } else {
                    $this->append_newline();
                }
            }
        }
        $this->append($token_text);
    }

    function handle_word($token_text) {

        if ($this->do_block_just_closed) {
            $this->append(' ');
            $this->append($token_text);
            $this->append(' ');
            $this->do_block_just_closed = false;
            return;
        }

        if ($token_text == 'function') {
            if ($this->flags->var_line) {
                $this->flags->var_line_reindented = !$this->options->keep_function_indentation;
            }

            if (($this->just_added_newline || $this->last_text == ';') && $this->last_text != '{') {
                # make sure there is a nice clean space of at least one blank line
                # before a new function definition
                $have_newlines = $this->n_newlines;
                if (!$this->just_added_newline) {
                    $have_newlines = 0;
                }
                if (!$this->options->preserve_newlines) {
                    $have_newlines = 1;
                }
                if ($have_newlines < 2) {
                    for ($i = 0; $i < 2 - $have_newlines; $i++) {
                        $this->append_newline(false);
                    }
                }
            }
        }

        if (in_array($token_text, Array('case', 'default'))) {
            if ($this->last_text == ':') {
                $this->remove_indent();
            } else {
                $this->flags->indentation_level--;
                $this->append_newline();
                $this->flags->indentation_level++;
            }
            $this->append($token_text);
            $this->flags->in_case = true;
            return;
        }

        $prefix = 'NONE';

        if ($this->last_type == TK_END_BLOCK) {
            if (!in_array($token_text, Array('else', 'catch', 'finally'))) {
                $prefix = 'NEWLINE';
            } else {
                if (in_array($this->options->brace_style, Array('expand', 'and-expand'))) {
                    $prefix = 'NEWLINE';
                } else {
                    $prefix = 'SPACE';
                    $this->append(' ');
                }
            }
        } elseif ($this->last_type == TK_SEMICOLON && in_array($this->flags->mode, Array('BLOCK', 'DO_BLOCK'))) {
            $prefix = 'NEWLINE';
        } elseif ($this->last_type == TK_SEMICOLON && $this->is_expression($this->flags->mode)) {
            $prefix = 'SPACE';
        } elseif ($this->last_type == TK_STRING) {
            $prefix = 'NEWLINE';
        } elseif ($this->last_type == TK_WORD) {
            if ($this->last_text == 'else') {
                # eat newlines between ...else *** some_op...
                # won't preserve extra newlines in this place (if any), but don't care that much
                $this->trim_output(true);
            }
            $prefix = 'SPACE';
        } elseif ($this->last_type == TK_START_BLOCK) {
            $prefix = 'NEWLINE';
        } elseif ($this->last_type == TK_END_EXPR) {
            $this->append(' ');
            $prefix = 'NEWLINE';
        }

        if ($this->flags->if_line && $this->last_type == TK_END_EXPR) {
            $this->flags->if_line = false;
        }

        if (in_array($token_text, $this->line_starters)) {
            if ($this->last_text == 'else') {
                $prefix = 'SPACE';
            } else {
                $prefix = 'NEWLINE';
            }
        }

        if (in_array($token_text, Array('else', 'catch', 'finally'))) {
            if ($this->last_type != TK_END_BLOCK ||
                $this->options->brace_style == 'expand' ||
                $this->options->brace_style == 'end-expand') {
                $this->append_newline();
            } else {
                $this->trim_output(true);
                $this->append(' ');
            }
        } elseif ($prefix == 'NEWLINE') {
            if ($token_text == 'function' && ($this->last_type == TK_START_EXPR || in_array($this->last_text, Array('=',',')))) {
                # no need to force newline on "function" -
                #   (function...
            } elseif ($token_text == 'function' && $this->last_text == 'new') {
                $this->append(' ');
            } elseif (in_array($this->last_text, Array('return', 'throw'))) {
                # no newline between return nnn
                $this->append(' ');
            } elseif ($this->last_type != TK_END_EXPR) {
                if (($this->last_type != TK_START_EXPR || $token_text != 'var') && $this->last_text != ':') {
                    # no need to force newline on VAR -
                    # for (var x = 0...
                    if ($token_text == 'if' && $this->last_word == 'else' && $this->last_text != '{') {
                        $this->append(' ');
                    } else {
                        $this->flags->var_line = false;
                        $this->flags->var_line_reindented = false;
                        $this->append_newline();
                    }
                }
            } elseif (in_array($token_text, $this->line_starters) && $this->last_text != ')') {
                $this->flags->var_line = false;
                $this->flags->var_line_reindented = false;
                $this->append_newline();
            }
        } elseif ($this->is_array($this->flags->mode) && $this->last_text == ',' && $this->last_last_text == '}') {
            $this->append_newline(); # }, in lists get a newline
        } elseif ($prefix == 'SPACE') {
            $this->append(' ');
        }

        $this->append($token_text);
        $this->last_word = $token_text;
        
        if ($token_text == 'var') {
            $this->flags->var_line = true;
            $this->flags->var_line_reindented = false;
            $this->flags->var_line_tainted = false;
        }

        if ($token_text == 'if') {
            $this->flags->if_line = true;
        }

        if ($token_text == 'else') {
            $this->flags->if_line = false;
        }

    }

    function restore_mode() {
        $this->do_block_just_closed = $this->flags->mode == 'DO_BLOCK';
        if (count($this->flag_store)) {
            $this->flags = array_pop($this->flag_store);
        }
    }


    function is_array($mode) {
        return in_array($mode, Array('[EXPRESSION]', '[INDENTED-EXPRESSION]'));
    }

    function is_expression($mode) {
        return in_array($mode, Array('[EXPRESSION]', '[INDENTED-EXPRESSION]', '(EXPRESSION)'));
    }

    function append_newline($ignore_repeated = true) {

        $this->flags->eat_next_space = false;

        if ($this->options->keep_array_indentation && $this->is_array($this->flags->mode)) {
            return;
        }

        $this->flags->if_line = false;
        $this->trim_output();

        if (count($this->output) == 0) {
            # no newline on start of file
            return;
        }

        if ($this->output[count($this->output)-1] != "\n" || !$ignore_repeated) {
            $this->just_added_newline = true;
            $this->output[] = "\n";
        }

        if ($this->preindent_string) {
            $this->output[] = $this->preindent_string;
        }

        for ($i = 0; $i < $this->flags->indentation_level; $i++) {
            $this->output[] = $this->indent_string;
        }

        if ($this->flags->var_line && $this->flags->var_line_reindented) {
            $this->output[] = $this->indent_string;
        }
    }

    function handle_string($token_text) {
        if (in_array($this->last_type, Array(TK_START_BLOCK, TK_END_BLOCK, TK_SEMICOLON))) {
            $this->append_newline();
        } elseif ($this->last_type == TK_WORD) {
            $this->append(' ');
        }

        # Try to replace readable \x-encoded characters with their equivalent,
        # if it is possible (e.g. '\x41\x42\x43\x01' becomes 'ABC\x01').

        # TODO: UNESCAPE!

        $this->append($token_text);
    }

    function handle_unknown($token_text) {
        if (in_array($this->last_text, Array('return', 'throw'))) {
            $this->append(' ');
        }

        $this->append($token_text);
    }

    function handle_operator($token_text) {
        $space_before = true;
        $space_after = true;

        if ($this->flags->var_line && $token_text == ',' && $this->is_expression($this->flags->mode)) {
            # do not break on comma, for ( var a = 1, b = 2
            $this->flags->var_line_tainted = false;
        }

        if ($this->flags->var_line && $token_text == ',') {
            if ($this->flags->var_line_tainted) {
                $this->append($token_text);
                $this->flags->var_line_reindented = true;
                $this->flags->var_line_tainted = false;
                $this->append_newline();
                return;
            } else {
                $this->flags->var_line_tainted = false;
            }
        }

        if (in_array($this->last_text, Array('return', 'throw'))) {
            # return had a special handling in TK_WORD
            $this->append(' ');
            $this->append($token_text);
            return;
        }

        if ($token_text == ':' && $this->flags->in_case) {
            $this->append($token_text);
            $this->append_newline();
            $this->flags->in_case = false;
            return;
        }

        if ($token_text == '::') {
            # no spaces around the exotic namespacing syntax operator
            $this->append($token_text);
            return;
        }

        if ($token_text == ',') {
            if ($this->flags->var_line) {
                if ($this->flags->var_line_tainted) {
                    # This never happens, as it's handled previously, right?
                    $this->append($token_start);
                    $this->append_newline();
                    $this->flags->var_line_tainted = false;
                } else {
                    $this->append($token_text);
                    $this->append(' ');
                }
            } elseif ($this->last_type == TK_END_BLOCK && $this->flags->mode != '(EXPRESSION)') {
                $this->append($token_text);
                if ($this->flags->mode == 'OBJECT' && $this->last_text == '}') {
                    $this->append_newline();
                } else {
                    $this->append(' ');
                }
            } else {
                if ($this->flags->mode == 'OBJECT') {
                    $this->append($token_text);
                    $this->append_newline();
                } else {
                    # EXPR or DO_BLOCK
                    $this->append($token_text);
                    $this->append(' ');
                }
            }
           # comma handled
           return;
        } elseif (in_array($token_text, Array('--', '++', '!')) ||
                  (in_array($token_text, Array('+', '-')) && in_array($this->last_type, Array(TK_START_BLOCK, TK_START_EXPR, TK_EQUALS, TK_OPERATOR))) ||
                  in_array($this->last_text, $this->line_starters)) {
            $space_before = false;
            $space_after = false;

            if ($this->last_text == ';' && $this->is_expression($this->flags->mode)) {
                # for (;; ++i)
                #         ^^
                $space_before = true;
            }

            if ($this->last_type == TK_WORD && in_array($this->last_text, $this->line_starters)) {
                $space_before = true;
            }

            if ($this->flags->mode == 'BLOCK' && in_array($this->last_text, Array('{', ';'))) {
                # { foo: --i }
                # foo(): --bar
                $this->append_newline();
            }
        } elseif ($token_text == '.') {
            # decimal digits or object.property
            $space_before = false;
        } elseif ($token_text == ':') {
            if ($this->flags->ternary_depth == 0) {
                $this->flags->mode = 'OBJECT';
                $space_before = false;
            } else {
                $this->flags->ternary_depth--;
            }
        } elseif ($token_text == '?') {
            $this->flags->ternary_depth++;
        }

        if ($space_before) {
            $this->append(' ');
        }

        $this->append($token_text);

        if ($space_after) {
            $this->append(' ');
        }
    }

    function handle_inline_comment($token_text) {
        $this->append(' ');
        $this->append($token_text);
        if ($this->is_expression($this->flags->mode)) {
            $this->append(' ');
        } else {
            $this->append_newline_forced();
        }
    }

    function handle_block_comment($token_text) {
        $lines = explode("\x0a", str_replace("\x0d", '', $token_text));

        # all lines start with an asterisk? that's a proper box comment
        $all_lines_start_with_asterisk = true;
        for ($i = 1; $i < count($lines); $i++) {
            if (trim($lines[$i]) == '' || substr(trim($lines[$i]), 0, 1) != '*') {
                $all_lines_start_with_asterisk = false;
            }
        }

        if ($all_lines_start_with_asterisk) {
            $this->append_newline();
            $this->append($lines[0]);
            for ($i = 1; $i < count($lines); $i++) {
                $this->append_newline();
                $this->append(' ' . trim($lines[$i]));
            }
        } else {
            # simple block comment: leave intact
            if (count($lines) > 1) {
                # multiline comment starts on a new line
                $this->append_newline();
                $this->trim_output();
             } else {
                # single line /* ... */ comment stays on the same line
                $this->append(' ');
            }
            foreach ($lines as $line) {
                $this->append($line);
                $this->append("\n");
            }
        }
        $this->append_newline();
    }

    function handle_comment($token_text) {
        if ($this->wanted_newline) {
            $this->append_newline();
        } else {
            $this->append(' ');
        }

        $this->append($token_text);
        $this->append_newline_forced();
    }


    function append($s) {
        if ($s == ' ') {
            # make sure only single space gets drawn
            if ($this->flags->eat_next_space) {
                $this->flags->eat_next_space = false;
            } elseif (count($this->output) && !in_array($this->output[count($this->output)-1], Array(' ', "\n", $this->indent_string))) {
                $this->output[] = ' ';
            }
        } else {
            $this->just_added_newline = false;
            $this->flags->eat_next_space = false;
            $this->output[] = $s;
        }
    }

    function append_newline_forced() {
        $old_array_indentation = $this->options->keep_array_indentation;
        $this->options->keep_array_indentation = false;
        $this->append_newline();
        $this->options->keep_array_indentation = $old_array_indentation;
    }

    function indent() {
        $this->flags->indentation_level++;
    }

    function remove_indent() {
        if (count($this->output) && in_array($this->output[count($this->output)-1], Array($this->indent_string, $this->preindent_string))) {
            array_pop($this->output);
        }
    }


}
