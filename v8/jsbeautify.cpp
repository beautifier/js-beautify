/*
    Copyright (C) 2010 Ariya Hidayat <ariya.hidayat@gmail.com>
    Copyright (c) 2009 Einar Lielmanis

    Permission is hereby granted, free of charge, to any person
    obtaining a copy of this software and associated documentation
    files (the "Software"), to deal in the Software without
    restriction, including without limitation the rights to use,
    copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following
    conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE.
 */

#include <v8.h>

#include "beautify.h"

using namespace v8;

int main(int argc, char* argv[])
{
    if (argc < 2) {
        printf("Usage: jsbeautify filename\n\n");
        return 0;
    }

    FILE* f = fopen(argv[1], "r");
    if (!f) {
        printf("Error: unable to open file %s\n", argv[1]);
        return 0;
    }
    int len = 0;
    while (!feof(f)) {
        fgetc(f);
        ++len;
    }
    rewind(f);
    char* buf = new char[len + 1];
    fread(buf, 1, len, f);
    fclose(f);

    HandleScope handle_scope;

    Handle<ObjectTemplate> global = ObjectTemplate::New();

    global->Set("code", String::New(buf, len));

    Handle<Context> context = Context::New(NULL, global);

    Context::Scope context_scope(context);

    Handle<Script> beautifyScript = Script::Compile(String::New(beautify_code));
    beautifyScript->Run();

    Handle<Script> runnerScript = Script::Compile(String::New("js_beautify(code)"));
    Handle<Value> result = runnerScript->Run();

    if (!result.IsEmpty() && !result->IsUndefined()) {
        String::Utf8Value str(result);
        printf("%s\n", *str);
    }

    delete [] buf;
    return 0;
}

