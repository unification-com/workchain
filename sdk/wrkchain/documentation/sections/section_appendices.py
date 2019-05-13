from wrkchain.documentation.sections.doc_section import DocSection


class SectionAppendices(DocSection):
    def __init__(self, section_number, title, wrkchain_name, mainchain_rpc_uri,
                 oracle_write_frequency, network, mainchain_network_id):
        path_to_md = 'appendices.md'
        DocSection.__init__(self, path_to_md, section_number, title)

        self.__section_number = section_number
        self.__sub_section_number = 1
        self.__wrkchain_name = wrkchain_name
        self.__mainchain_rpc_uri = mainchain_rpc_uri
        self.__oracle_write_frequency = oracle_write_frequency
        self.__network = network
        self.__mainchain_network_id = mainchain_network_id

    def generate(self):

        appendix_1 = self.__appendix_1()
        appendix_2 = self.__appendix_2()
        appendix_3 = self.__appendix_3()
        appendix_4 = self.__appendix_4()
        appendix_5 = ''
        if self.__network != 'eth':
            appendix_5 = self.__appendix_5()

        d = {
            '__APPENDIX_1__': appendix_1,
            '__APPENDIX_2__': appendix_2,
            '__APPENDIX_3__': appendix_3,
            '__APPENDIX_4__': appendix_4,
            '__APPENDIX_5__': appendix_5,
        }
        self.add_content(d, append=False)
        return self.get_contents()

    def __appendix_1(self):
        md_file = 'sub/appendices/appendix1.md'
        t = self.load_sub_section_template(md_file)
        contents = t.substitute(
            {'__SECTION_NUMBER__': self.__section_number,
             '__SUB_SECTION_NUMBER__': self.__sub_section_number})
        self.__sub_section_number += 1
        return contents

    def __appendix_2(self):
        md_file = 'sub/appendices/appendix2.md'
        t = self.load_sub_section_template(md_file)
        contents = t.substitute(
            {'__SECTION_NUMBER__': self.__section_number,
             '__SUB_SECTION_NUMBER__': self.__sub_section_number})
        self.__sub_section_number += 1
        return contents

    def __appendix_3(self):
        md_file = 'sub/appendices/appendix3.md'
        t = self.load_sub_section_template(md_file)
        contents = t.substitute(
            {'__SECTION_NUMBER__': self.__section_number,
             '__SUB_SECTION_NUMBER__': self.__sub_section_number,
             '__MAINCHAIN_WEB3_PROVIDER_URL__': self.__mainchain_rpc_uri,
             '__WRKCHAIN_NAME__': self.__wrkchain_name,
             '__ORACLE_WRITE_FREQUENCY__': self.__oracle_write_frequency
             })
        self.__sub_section_number += 1
        return contents

    def __appendix_4(self):
        md_file = 'sub/appendices/appendix4.md'
        t = self.load_sub_section_template(md_file)
        contents = t.substitute(
            {'__SECTION_NUMBER__': self.__section_number,
             '__SUB_SECTION_NUMBER__': self.__sub_section_number})
        self.__sub_section_number += 1
        return contents

    def __appendix_5(self):
        md_file = 'sub/appendices/appendix5.md'
        t = self.load_sub_section_template(md_file)

        und_network_flag = ''
        und_genesis_json = 'und-testnet-50005'
        if self.__network == 'testnet':
            und_network_flag = '--und-testnet'
            und_genesis_json = 'und-testnet-50005'

        contents = t.substitute(
            {'__SECTION_NUMBER__': self.__section_number,
             '__SUB_SECTION_NUMBER__': self.__sub_section_number,
             '__MAINCHAIN_NETWORK__': self.__network,
             '__MAINCHAIN_NETWORK_ID__': self.__mainchain_network_id,
             '__UND_NETWORK_FLAG__': und_network_flag,
             '__UND_GENESIS_JSON__': und_genesis_json
             })
        self.__sub_section_number += 1
        return contents


class SectionAppendicesBuilder:
    def __init__(self):
        self.__instance = None

    def __call__(self, section_number, title, wrkchain_name, mainchain_rpc_uri,
                 oracle_write_frequency, network, mainchain_network_id,
                 **_ignored):
        if not self.__instance:
            self.__instance = SectionAppendices(section_number, title,
                                                wrkchain_name,
                                                mainchain_rpc_uri,
                                                oracle_write_frequency,
                                                network, mainchain_network_id)

        return self.__instance
