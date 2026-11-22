import json,re
D='/tmp/claude-0/-home-user-app-policies/08207d95-5f38-5913-acec-14c31ee115ad/scratchpad/data/'
a=json.load(open(D+'arrivals.json'))
a=[x for x in a if x[0]>='2021-01-01']
# drop duplicate Carnival (artist credit change Kanye West -> Ye); first top-10 week is 2024-02-24
a=[x for x in a if not (x[2]=='Carnival' and x[0]=='2024-03-23')]
NONRAP=['Taylor Swift','Morgan Wallen','Olivia Rodrigo','Ariana Grande','Sabrina Carpenter','Tate McRae','Harry Styles','Bruno Mars','Zach Bryan','Chappell Roan','Noah Kahan','Ella Langley','BTS','Jimin','Billie Eilish','Beyonce','Miley Cyrus','Bad Bunny','Karol G','Grupo Frontera','Eslabon Armado','Bizarrap','Luke Combs','Bailey Zimmerman','Jason Aldean','Oliver Anthony','Dua Lipa','Teddy Swims','Benson Boone','Hozier','Gracie Abrams','Lady Gaga','ROSE','Alex Warren','Justin Bieber','Ed Sheeran','Adele','Coldplay','Glass Animals','Kate Bush','Joji','OneRepublic','Nicky Youre','Sam Smith','Elton John','Rihanna','Kelly Clarkson','Dean Martin','Nat King Cole','Wham!','Chuck Berry','Jose Feliciano','The Ronettes','Carolina Gaitan','Jessica Darrow','GAYLE','JVKE','Rema','Tyla','Wizkid','Djo','sombr','Olivia Dean','Kehlani','Leon Thomas','Ravyn Lenae','HUNTR/X','Saja Boys','Tame Impala','Silk Sonic','AJR','Shawn Mendes','The Beatles','Walker Hayes','Shaboozey','David Guetta','Steve Lacy','Koe Wetzel','Ashe']
SOLO_NONRAP={('Die For You','The Weeknd'),('Take My Breath','The Weeknd'),('Save Your Tears','The Weeknd & Ariana Grande'),
 ('Kill Bill','SZA'),('Nobody Gets Me','SZA'),('Saturn','SZA'),('Snooze','SZA'),('I Hate U','SZA'),('Good Days','SZA'),
 ('Without You','The Kid LAROI'),('Stay','The Kid LAROI & Justin Bieber'),('I Had Some Help','Post Malone Featuring Morgan Wallen'),
 ('Standing Next To You','Jung Kook'),('Lift Me Up','Rihanna')}
CLOSE={'Whisper My Name','Nokia','30 For 30','Rather Lie','All The Way','Luther','Timeless','Million Dollar Baby','Act II: Date @ 8','Agora Hills',
 '3D','Slime You Out','Paint The Town Red','K-POP','Seven','Barbie World','Favorite Song','Boy\'s A Liar, Pt. 2','Creepin\'','Superhero (Heroes & Villains)',
 'Spin Bout U','Vegas','Bad Decisions','Sticky','Falling Back','I Like You (A Happier Song)','Die Hard','Wait For U','Woman','Enemy','Need To Know',
 'One Right Now','Thats What I Want','Rumors','Industry Baby','Kiss Me More','Montero (Call Me By Your Name)','34+35','Calling My Phone','Peaches',
 'Forever','TSU','In The Bible','Champagne Poetry','Fair Trade','St. Chroma','Young Metro','Holy','Boston','Nicole Kidman','Babydoll','Stateside',
 'Solar Eclipse','What You Know Bout Love','Astronaut In The Ocean','Mutt','Folded','Water','Essence','Calm Down','Bad Habit','Lemonade'}
out=[]
for d,pos,song,art,lw,woc in a:
    prim=art
    if (song,art) in SOLO_NONRAP: prior='nonrap'
    elif any(art.startswith(n) for n in NONRAP) and song not in CLOSE: prior='nonrap'
    elif song in CLOSE: prior='close'
    else: prior='rap'
    out.append(dict(first_top10=d,rank=pos,title=song,artist=art,prior=prior))
json.dump(out,open(D+'candidates.json','w'),indent=1)
from collections import Counter
print(Counter(o['prior'] for o in out))
# running count of rap+close from newest
n=0
for o in out:
    if o['prior']!='nonrap':
        n+=1
        print(n,o['first_top10'],o['rank'],o['title'],'|',o['artist'],'|',o['prior'])
