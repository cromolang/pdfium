"""Writes the PDF of the tests by hand: two pages, the first of 300 by 200 points with
a line of text and a red square, the second of 200 by 300 with another line; a title
and an author in its information.

    python tools/sample.py testdata/sample.pdf
"""
import sys


def stream(text):
    data = text.encode('latin-1')
    return b'<< /Length %d >>\nstream\n' % len(data) + data + b'\nendstream'


objects = [
    b'<< /Type /Catalog /Pages 2 0 R >>',
    b'<< /Type /Pages /Kids [3 0 R 5 0 R] /Count 2 >>',
    b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 200] /Contents 4 0 R /Resources << /Font << /F1 7 0 R >> >> >>',
    stream('BT /F1 24 Tf 20 150 Td (Hello from Cromo) Tj ET\n1 0 0 rg 20 20 60 60 re f'),
    b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 200 300] /Contents 6 0 R /Resources << /Font << /F1 7 0 R >> >> >>',
    stream('BT /F1 18 Tf 20 250 Td (The second page) Tj ET'),
    b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',
    b'<< /Title (A sample for the tests) /Author (Cromo) >>',
]
out = bytearray(b'%PDF-1.4\n')
offsets = []
for number, body in enumerate(objects, 1):
    offsets.append(len(out))
    out += b'%d 0 obj\n' % number + body + b'\nendobj\n'
start = len(out)
out += b'xref\n0 %d\n' % (len(objects) + 1)
out += b'0000000000 65535 f \n'
for offset in offsets:
    out += b'%010d 00000 n \n' % offset
out += b'trailer\n<< /Size %d /Root 1 0 R /Info 8 0 R >>\nstartxref\n%d\n%%%%EOF\n' % (len(objects) + 1, start)
open(sys.argv[1], 'wb').write(out)
print(len(out), 'bytes')
