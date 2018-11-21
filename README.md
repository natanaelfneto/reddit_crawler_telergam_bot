## Crawlers

### Parte 1

O script presente no arquivo 'crawlers/Python/src/reddit_crawler.py' soluciona a parte 1, devendo ser executado por linha de comando:
```Shell
python reddit_crawler.py [threads]
```

dependências:
- beautifulsoup4==4.6.3
- lxml==4.2.5

O uso pode ser notado de acordo com a tabela:

| Campo       | Obrigatório   | Descrição                               | Valor mínimo de upvotes
| ---         | ---           | ---                                     | ---
| threads     | sim           | nomes de threads a serem vasculhadas    | 5000

Exemplo:
```Shell
python reddit_crawler.py cats dogs
```

resultado examplo:
```json
URL: https://www.reddit.com/r/cats
STATUS: 200
REASON: OK

URL: https://www.reddit.com/r/dogs
STATUS: 200
REASON: OK

{
    "cats": [
        {
            "commentaries_link": "https://www.reddit.com/r/cats/comments/9nitmu/my_first_rescue_i_guess_im_gonna_be_a_catdad/",
            "subreddit": "cats",
            "subthread_link": "https://www.reddit.com/r/cats/search?q=flair_name%253A%2522Cat%2520Picture%2522&restrict_sr=1",
            "title": "My first rescue I guess I'm gonna be a catdad...",
            "upvotes": "7.8k"
        }
    ]
},
{
    "dogs": []
}
```

### Parte 2

A parte 2 foi solucionada utilizando o script da parte 1 como modulo python, acrescido de um script para o bot, telegram.py

dependências:
- beautifulsoup4==4.6.3
- lxml==4.2.5
- telepot==12.7

Para inicial o bot use o commando:
```Shell
python telegram.py <bot_token>
```
Incie uma conversa com o bot, pela aplicação do telegram: @your_chosen_name_bot. Envie o commando na janela do chat:
```Shell
/nadaprafazer [+ args]
```
O uso mp chat pode ser notado de acordo com a tabela:

| Comando/mensagem  | Aceita multiplos argumentos   | Descrição                               | Valor mínimo de upvotes
| ---               | ---                           | ---                                     | ---
| /nadaprafazer     | sim                           | retorna posts de threads no reddit      | 5000
| *                 | não                           | retorna mensagem de erro                |

_mensagem padrão de erro no chat: "Desculpe, não entendi."_

Resultado como exemplo:
```Shell
/nadaprafazer cats.    brazil cats
```
o exemplo irá resultar no console:
```ShellSession
Starting reddit_crawler_bot
Author: natanaelfneto
Description: An apprentice scrapper bot

Waiting for inputs...

INPUT:
        content type: text
        type: private
        chat id: 298223493
        pending requests: 4

URL: https://www.reddit.com/r/cats.
STATUS: 404
REASON: Not Found
No server response
1 out of 4 request sent

URL: https://www.reddit.com/r/brazil
STATUS: 200
REASON: OK
Attempt 1...

URL: https://www.reddit.com/r/brazil
STATUS: 200
REASON: OK
Attempt 2...

URL: https://www.reddit.com/r/brazil
STATUS: 200
REASON: OK
Attempt 3...

URL: https://www.reddit.com/r/cats
STATUS: 200
REASON: OK
4 out of 4 request sent
```

E responderá no telegram:

THREAD: **cats.** [thread link](http://www.reddit.com/r/cats./)\
    No threads with more than 5k upvotes could be retrieved, try again in a few minutes

THREAD: **brazil** [thread link](http://www.reddit.com/r/brazil/)\
    No threads with more than 5k upvotes could be retrieved, try again in a few minutes

THREAD: **cats** [thread link](http://www.reddit.com/r/cats/)
        
**title**: The scent of spring\
**upvotes**: 5.8k\
link to commentaries: [link](https://www.reddit.com/r/cats/comments/9nswzp/the_scent_of_spring_by_natalya_bachkova_1200x866/)\
link to subthread: [link](https://www.reddit.com/r/cats/search?q=flair_name%253A%2522Cat%2520Picture%2522&restrict_sr=1)

**title**: Not this year\
**upvotes**: 11.3k\
link to commentaries: [link](https://www.reddit.com/r/cats/comments/9nocwr/not_this_year/)\
link to subthread: [link](https://www.reddit.com/r/cats/search?q=flair_name%253A%2522Cat%2520Picture%2522&restrict_sr=1)

**title**: Recently lost my two cats that my wife and I had for 10 years. The house felt too empty so we got these two floofs to bring some energy back to the home.\
**upvotes**: 9.4k\
link to commentaries: [link](https://www.reddit.com/r/cats/comments/9nmevi/recently_lost_my_two_cats_that_my_wife_and_i_had/)\
link to subthread: [link](https://www.reddit.com/r/cats/search?q=flair_name%253A%2522Mourning%252FLoss%2522&restrict_sr=1)