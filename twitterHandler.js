import Twitter from "twitter";
import { twitAuth } from './auth.js';
import { client } from './index.js';


export async function twitterStream() {
    let msgGuild, msgchannel;
    let toSend = ["704096220359950456","887011763382521888"];
    msgGuild = await client.guilds.cache.get(toSend[0]);
    msgchannel = await msgGuild.channels.cache.get(toSend[1]);
    let Twit = new Twitter(twitAuth);
    Twit.stream('statuses/filter', { follow: '1155846185535643649' }, function (stream) {
        stream.on('data', function (tweet) {
            msgchannel.send(tweet.text);
        });

        stream.on('error', function (error) {
            console.log(error);
        });
    });
}
