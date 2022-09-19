import tempfile as tmpf
import shutil

def addTags(tags, file):
    #print("Adding tags to " + file)

    fout = tmpf.NamedTemporaryFile("wb", dir=".", delete=False)
    file = open(file, "rb")

    try:
        fout.write(file.read(2))
        while True:
            buf = file.read(4)
            fout.write(buf)
            print(b'\xFF')
            if buf[0] == 255 and buf[1] == 225:
                print("Offset: " + str((buf[2] * 256 + buf[3]) - 2))
                buf_str = file.read((buf[2] * 256 + buf[3]) - 2)
                step = buf_str.find(b'http://ns.adobe.com/xap/1.0/\x00')
                if step != -1:
                    step += len(b'http://ns.adobe.com/xap/1.0/\x00')
                    print("XMP tag found~!")
                    step_inc = buf_str[step:].find(b'<dc:subject>')
                    step += buf_str[step:].find(b'<dc:subject>') + len(b'<dc:subject>')
                    if step_inc != -1:
                        step_inc = buf_str[step:].find(b'<rdf:Bag>')
                        step += buf_str[step:].find(b'<rdf:Bag>') + len(b'<rdf:Bag>')
                        if step_inc != -1:
                            print("adding my keyword!")
                            new_buf_str = buf_str[:step]
                            for tag in tags:
                                new_buf_str += b'\n    <rdf:li>' + tag.encode('utf_8') + b'</rdf:li>' 
                            new_buf_str += buf_str[step:]
                            #buf_str = b'\xff\xe1' + (len(buf_str) + 2).to_bytes(2, 'big') + new_buf_str
                            fout.write(new_buf_str)
                            fout.write(file.read())
                            break
                        else:
                            print("This XMP tag has no keyword bag!")
                            step = buf_str[step:].find(b'</dc:subject>')
                            new_buf_str = buf_str[:step] + '''   <rdf:Bag>'''.encode('utf_8')
                            for tag in tags:
                                new_buf_str += buf_str[:step] + b'\n    <rdf:li>' + tag.encode('utf_8') + b'</rdf:li>' + buf_str[step:]
                            new_buf_str += '''
   </rdf:Bag>'''.encode('utf_8') + buf_str[step:]
                            #buf_str = b'\xff\xe1' + (len(buf_str) + 2).to_bytes(2, 'big') + new_buf_str
                            fout.write(new_buf_str)
                            fout.write(file.read())
                            break
                    else:
                        print("This XMP tag has no dc description!")
                        step = buf_str.find[step:](b'</rdf:RDF>') 
                        new_buf_str = buf_str[:step] + ''' <rdf:Description rdf:about=''
  xmlns:dc='http://purl.org/dc/elements/1.1/'>
  <dc:subject>
   <rdf:Bag>'''.encode('utf_8')
                        for tag in tags:
                            new_buf_str += buf_str[:step] + b'\n    <rdf:li>' + tag.encode('utf_8') + b'</rdf:li>' + buf_str[step:]
                        new_buf_str += '''
   </rdf:Bag>
  </dc:subject>
 </rdf:Description>'''.encode('utf_8') + buf_str[step:]
                        #buf_str = b'\xff\xe1' + (len(buf_str) + 2).to_bytes(2, 'big') + new_buf_str
                        fout.write(new_buf_str)
                        fout.write(file.read())
                        break
                #else:
                    #print("This FFE1 tag does not have XMP data")
                    
                fout.write(buf_str)
            else:
                print("Tag xFFE1 not found, found " + buf[0].to_bytes(1, "little").hex() + buf[1].to_bytes(1, "little").hex() + " instead, skipping ahead " + str((buf[2] * 256 + buf[3]) - 2) + " bytes")
                fout.write(file.read((buf[2] * 256 + buf[3]) - 2))
    except:
        #No XMP data found 
        #print("No proper XMP tags found, will have to add them...")
        file_name = file.name
        file.close()
        file = open(file_name, "rb")
        fout.close()
        fout = tmpf.NamedTemporaryFile("wb", dir=".", delete=False)
        buf = file.read(2)
        fout.write(buf)
        #print("WRITING: " + buf.hex())
        buf = file.read(4)
        #print("Tag: " + buf[0].to_bytes(1, "little").hex() + buf[1].to_bytes(1, "little").hex())
        if buf[0] == 255 and buf[1] == 224:
            #print("First tag is 0xFFE0, going to next tag")
            fout.write(buf)
            buf = file.read((buf[2] * 256 + buf[3]) - 2)
            fout.write(buf)
            #print("WRITING: " + buf.hex())
            buf = file.read(4)
            #print("Next tag is " + buf[0].to_bytes(1, "little").hex() + buf[1].to_bytes(1, "little").hex())
        if buf[0] == 255 and buf[1] == 225:
            #print("Next tag is 0xFFE1, going to next tag")
            fout.write(buf)
            buf = file.read((buf[2] * 256 + buf[3]) - 2)
            fout.write(buf)
            #print("WRITING: " + buf.hex())
            buf = file.read(4)
            #print("Next tag is " + buf[0].to_bytes(1, "little").hex() + buf[1].to_bytes(1, "little").hex())
        old_marker = buf
        xmp_string = '''http://ns.adobe.com/xap/1.0/\x00<?xpacket begin='' id='W5M0MpCehiHzreSzNTczkc9d'?>
<x:xmpmeta xmlns:x='adobe:ns:meta/' x:xmptk='Image::ExifTool 12.44'>
<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>

 <rdf:Description rdf:about=''
  xmlns:dc='http://purl.org/dc/elements/1.1/'>
  <dc:subject>
   <rdf:Bag>
'''.encode('utf_8')
    
        for tag in tags:
            xmp_string += b'    <rdf:li>' + tag.encode('utf_8') + b'</rdf:li>\n'
        
        xmp_string += '''
   </rdf:Bag>
  </dc:subject>
 </rdf:Description>
</rdf:RDF>
</x:xmpmeta>
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
<?xpacket end='w'?>'''.encode('utf_8')

        xmp_string = b'\xff\xe1' + (len(xmp_string) + 2).to_bytes(2, 'big') + xmp_string
        #print("XMP String written, writting to file")
        #print("WRITING: " + xmp_string[:4].hex() + xmp_string[4:].decode('utf-8') + old_marker[:4].hex())
        fout.write(xmp_string + old_marker)
        buf = file.read()
        #print("WRITING: " + buf.hex())
        fout.write(buf)
    
    #print("Closing temp file and replacing old file")
    fout.close()
    shutil.move(fout.name, file.name)