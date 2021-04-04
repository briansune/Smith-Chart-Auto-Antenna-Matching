import configparser as cfg


class MatchCal:

    def __init__(self):
        self.config = cfg.ConfigParser()
        self.check4cfg()

    def check4cfg(self):
        try:
            with open('cmp_list.ini') as f:
                self.config.read_file(f)
        except IOError:
            self.config['component'] = {'C 0402': '[0.5, 1.0, 1.2, 1.5, '
                                                  '1.8, 2.2, 2.7, 3.0, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]',
                                        'L 0402':
                                            '[1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 7.8]'}
            with open('cmp_list.ini', 'w') as cff:
                self.config.write(cff)
