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

#include <QtScript>

#include <iostream>

static QString readFile(const QString &fileName)
{
    QFile file;
    file.setFileName(fileName);
    if (!file.open(QFile::ReadOnly)) {
        std::cerr << "Can't open" << qPrintable(fileName) << std::endl;
        return QString();
    }
    QString content = file.readAll();
    file.close();
    return content;
}

int main(int argc, char **argv)
{
    QCoreApplication app(argc, argv);

    if (argc < 2) {
        std::cout << "Usage:" << std::endl << std::endl;
        std::cout << "    jsbeautify source-file" << std::endl << std::endl;
        return 0;
    }

    QString script = readFile(":/beautify.js");
    QString source = readFile(QString::fromLocal8Bit(argv[1]));

    if (!script.isEmpty() && !source.isEmpty()) {
        QScriptEngine engine;
        engine.evaluate(script);
        engine.globalObject().setProperty("source", QScriptValue(source));
        QScriptValue result = engine.evaluate("js_beautify(source);");
        std::cout << qPrintable(result.toString()) << std::endl;
    }

    return 0;
}

