import struct
from PIL import Image
import os
import argparse


def parse_config():
    parser = argparse.ArgumentParser(description="RAF2JPEG")
    parser.add_argument('--input', '-i', type=str, required=True, help="input directory address") 
    parser.add_argument('--output', '-o', type=str, required=True, help="export directory address") 
    args = parser.parse_args()
    return args


class RAFHeader:
    # .RAF basic information
    def __init__(self, filename):
        with open(filename, 'rb') as f:
            self.type_string = struct.unpack('>16s', f.read(16))[0]
            self.format_ver = struct.unpack('>4s', f.read(4))[0]
            self.camera_id = struct.unpack('>8s', f.read(8))[0]
            self.camera_str = struct.unpack('>32s', f.read(32))[0].decode("utf_8")
            self.offset_ver = struct.unpack('>4s', f.read(4))[0]
            self.offset_unk = struct.unpack('>20s', f.read(20))[0].decode("utf_8")
            self.offset_jpg_offset = struct.unpack('>1i', f.read(4))[0]
            self.offset_jpg_length = struct.unpack('>1i', f.read(4))[0]
            self.offset_CFA_header_offset = struct.unpack('>1i', f.read(4))[0]
            self.offset_CFA_header_length = struct.unpack('>1i', f.read(4))[0]
            self.offset_CFA_offset = struct.unpack('>1i', f.read(4))[0]
            self.offset_CFA_length = struct.unpack('>1i', f.read(4))[0]


class JPEG:
    # Exif JFIF with thumbnail + preview
    def __init__(self, filename, offset, length):
        with open(filename, 'rb') as f:
            f.seek(offset)
            self.bin = f.read(length)

    def exif(self):
        pass
        # todo


class CFA:
    def __init__(self, filename, header_offset, header_length, data_offset, data_length):
        self.filename = filename
        self.data_offset = data_offset
        self.data_length = data_length
        self.records = []
        with open(filename, 'rb') as f:
            f.seek(header_offset)
            self.count = struct.unpack('>1i', f.read(4))[0]
            for record in range(self.count):
                tag = struct.unpack('>1H', f.read(2))[0]
                size = struct.unpack('>1H', f.read(2))[0]
                self.records.append({"id": tag, "size": size, "data": f.read(size)})
            pass

    def unpack(self):
        with open(self.filename, 'rb') as f:
            f.seek(self.data_offset)
            # todo


class RAF:
    def __init__(self, filename):
        self.filename = filename
        self.header = RAFHeader(filename)
        self.jpg = JPEG(filename, self.header.offset_jpg_offset, self.header.offset_jpg_length)
        self.CFA = CFA(filename, self.header.offset_CFA_header_offset, self.header.offset_CFA_header_length,
                       self.header.offset_CFA_offset, self.header.offset_CFA_length)

    def __export_exif(self, path):
        jpg_bin = self.jpg.bin
        # todo

    def __export_jpg(self, path):
        with open(path, "wb") as f:
            f.write(self.jpg.bin)

    def __export_dng(self, path):
        self.CFA.unpack()
        # todo

    def export(self, path, suffix):
        eval("self._RAF__export_"+suffix.lower()+"('"+path+'.'+suffix+"')")


if __name__ == '__main__':
    args = parse_config()
    export_path = args.output
    import_path = args.input
    if not os.path.exists(export_path):
        os.mkdir(export_path)
    file_lst = os.listdir(import_path)
    for i, name in enumerate(file_lst):
        if name.split(".")[-1] == "RAF":
            file_path = import_path + name
            obj = RAF(file_path)
            export_path = export_path + name.split(".")[0]
            obj.export(export_path, 'jpg')
    pass

