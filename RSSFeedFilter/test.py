from ps7 import *

koala     = NewsStory('', 'Koala bears are soft and cuddly', '', '', '')
pillow    = NewsStory('', 'I prefer pillows that are soft.', '', '', '')
soda      = NewsStory('', 'Soft drinks are great', '', '', '')
pink      = NewsStory('', "Soft's the new pink!", '', '', '')
football  = NewsStory('', '"Soft!" he exclaimed as he threw the football', '', '', '')
microsoft = NewsStory('', 'Microsoft announced today that pillows are bad', '', '', '')
nothing   = NewsStory('', 'Reuters reports something really boring', '', '' ,'')
caps      = NewsStory('', 'soft things are soft', '', '', '')

s1 = TitleTrigger('SOFT')
print s1.evaluate(microsoft)