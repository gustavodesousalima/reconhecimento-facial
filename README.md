# Look-ID

## Sobre Nós

Somos um grupo de alunos apaixonados por tecnologia e inovação, que criaram a plataforma **Look-ID** para oferecer uma experiência de reconhecimento facial acessível e segura.

## O Que É a Look-ID?

A **Look-ID** permite que os usuários subam uma imagem e testem o reconhecimento facial em nossa plataforma. Nosso objetivo é simplificar o acesso à tecnologia de reconhecimento facial, garantindo a privacidade e a segurança das informações dos usuários.

## Compromisso com a Privacidade

Nosso compromisso é **não utilizar** as informações pessoais de nossos usuários para nenhum propósito além do reconhecimento facial. Valorizamos a transparência e a confiança, e estamos sempre buscando maneiras de melhorar nossos serviços e proteger os dados dos nossos usuários.


## Modelo de configuração do Nginx 

Caminho: /etc/nginx/sites-available/default

server {
    listen 443 ssl;
    server_name lookid.com.br;

    ssl_certificate /etc/letsencrypt/live/lookid.com.br/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/lookid.com.br/privkey.pem;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 80;
    server_name lookid.com.br;
    return 301 https://$host$request_uri;
}

## Agradecimento

Agradecemos por escolher a **Look-ID**! Juntos, estamos moldando o futuro do reconhecimento facial.

<h1 style="text-align: center;">Tecnologias Usadas</h1>
            <div align="center" style= "display: inline_block"><br/>
                <img loading="lazy" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/html5/html5-plain.svg" height="60" width="60" />
                <img loading="lazy" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/css3/css3-plain.svg" height="60" width="60" />
                <img loading="lazy" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-plain.svg" height="60" width="60" />
                <img loading="lazy" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/git/git-original.svg" height="60" width="60" />
                <img loading="lazy" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" height="60" width="60" /><br><br>
                <h1 style="text-align: center;"> Provedores Cloud</h1>
                <img loading="lazy" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/googlecloud/googlecloud-original.svg" height="60" width="60" />
                <img loading="lazy" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/amazonwebservices/amazonwebservices-plain-wordmark.svg" height="60" width="60" /><br><br>
                <h1 style="text-align: center;"> IDEs</h1>
                <img loading="lazy" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/vscode/vscode-original.svg" height="60" width="60" />
                <img loading="lazy" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/pycharm/pycharm-original.svg" height="60" width="60" />
            </div>