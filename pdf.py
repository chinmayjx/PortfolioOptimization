from PyPDF2 import PdfFileReader, PdfFileWriter
import matplotlib.pyplot as plt


class PDF:
    def __init__(self, name, show):
        self.rr = None
        self.wr = PdfFileWriter()
        self.name = name
        self.show = show

    def add(self):
        plt.savefig("pdf/temp.pdf")
        if self.show:
            plt.show()
        plt.clf()
        self.rr = PdfFileReader("pdf/temp.pdf")
        self.wr.addPage(self.rr.getPage(0))

    def save(self):
        fl = open(self.name, "bw")
        self.wr.write(fl)
