/*
 * unpacker for scripts that went through javascript2img.com
 *
 * the packer is very creative at packing JS (it encodes it in a PNG image) however it's pretty shitty nonetheless:
 *  alert("%3D") alerts "="
 *  alert("%253D") also alerts "="
 *  alert("%%") won't run and throw URIError: URI malformed
 * this module will unpack scripts the correct way though
 *
 * another one: if the base64 of the PNG image the packer generates contains // somewhere it will be cut off there and you'll get invalid js
 */


var javascript2img = {
	detect: function (str) {
		if(/v[a-f0-9]{32}\[0\]\.getContext/.test(str)) {
			return true;
		}
		return false;
	},

	unpack: function (str) {
		if (!javascript2img.detect(str))
			return str;
		// Get png data
		var rmatch = /'cmV0dXJuJTIwJ2RhdGElM0FpbWFnZSUyRnBuZyUzQmJhc2U2NCUyQyclM0I=', '', '([A-Za-z0-9+\/=]+)'/.exec(str);
		if (!rmatch)
			return str;
		var img = this._decode_base64_png(rmatch[1]);
		if (img === false)
			return str;
		// Get decode function
		var rmatch = /'(Zm9yKH[A-Za-z0-9+\/=]+)'/.exec(str);
		if (!rmatch)
			return str;
		var decodefunc = unescape(this._decode_base64(rmatch[1]));
		// Find out how the decode function works and act accordingly
		// TODO: Are there other strategies employed by the packer?
		if (this._check_decodefunc("for(%var%=%var%.data.length-1;%var%>=%var%[0];%var%--)", decodefunc)) {
			var d_start = img.data.length - 1;
			var d_cond = function(i) { return i >= 0 };
			var d_step = -1;
		} else if (this._check_decodefunc("for(%var%=%var%[2]; %var% < %var%.data.length; %var%+=4)", decodefunc)) {
			// Get start index
			var rmatch = /v[a-f0-9]{32}=\[0,255,([0-9]+)\];/.exec(str);
			if (!rmatch)
				return str;
			var d_start = parseInt(rmatch[1]);
			var d_cond = function(i) { return i < img.data.length };
			var d_step = 4;
		} else {
			//console.log("unknown decodefunc type\n------\n%s\n------", decodefunc.replace(/v([a-f0-9]{4})[a-f0-9]{28}/g, "%$1%"));
			return str;
		}
		// Decode pixel data
		str = "";
		for (var i = d_start; d_cond(i); i += d_step) {
			if (img.data[i] != 255)
				str += String.fromCharCode(img.data[i]);
		}
		return this._decode_base64(str);
	},

	_decode_base64: function (str) {
		if (typeof window !== 'undefined')
			return window.atob(str);
		else
			return (new Buffer(str, 'base64')).toString('utf-8');
	},

	_decode_base64_png: function (str) {
		if (typeof window !== 'undefined') {
			var img = document.createElement("img");
			img.src = "data:image/png;base64," + str;
			img.style.display = "none";
			document.body.appendChild(img);
			var cnv = document.createElement("canvas");
			cnv.width = img.width;
			cnv.height = img.height;
			cnv.style.display = "none";
			document.body.appendChild(cnv);
			var ctx = cnv.getContext("2d");
			ctx.drawImage(img, 0, 0);
			var data = ctx.getImageData(0, 0, cnv.width, cnv.height);
			img.remove();
			cnv.remove();
			return data;
		} else {
			try {
				var PNG = require('pngjs2').PNG;
			} catch(e) {
				console.warn("Warning: javascript2img-packed code was detected but could not be unpacked due to missing modules.");
				console.warn("         Please install pngjs2 with npm.");
				return false;
			};
			var buf = new Buffer(str, 'base64');
			return PNG.sync.read(buf);
		}
	},

	_check_decodefunc: function (rule, decodefunc) {
		var r = rule;
		r = r.replace(/[-[\]{}()*+?.\\^$|#\s]/g, "\\$&");
		r = r.replace(/%var%/g, "v[a-f0-9]{32}");
		r = "^" + r;
		var m = (new RegExp(r)).test(decodefunc);
		//if(m)
		//	console.log("rule match: %s", rule);
		return m;
	},

	run_tests: function (sanity_test) {
		var t = sanity_test || new SanityTest();

		t.test_function(this._decode_base64, "javascript2img._decode_base64");
		t.expect("Zmx1ZmZ5", "fluffy");
		t.test_function(function(a) {return javascript2img._check_decodefunc(a[0], a[1])}, "javascript2img._check_decodefunc");
		t.expect(["%var% = %var%;", ""], false);
		t.expect(["%var% = %var%;", "foo = bar;"], false);
		t.expect(["%var% = %var%;", "v0a63761d20b234e464ed87e282c4eec3 = v9590e2cf04e941a01b43d16391df12b0;"], true);
		t.expect(["...", "aaa"], false);
		t.expect(["...", "..."], true);
		t.expect(["[a-z]", "q"], false);
		t.expect(["[a-z]", "[a-z]"], true);
		t.test_function(this.detect, "javascript2img.detect");
		t.expect("", false);
		t.expect(".getContext", false);
		t.expect("foo[0].getContext", false);
		t.expect("v3a384a1588bf81a10206fb3c7aa8315a[0].getContext", true);

		return t;
	}
};

if (typeof exports !== 'undefined')
	exports.javascript2img = javascript2img;
