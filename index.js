import { token } from './auth.js'
import { Client, Intents, MessageEmbed } from 'discord.js';
import { PassThrough } from 'stream';
const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES, Intents.FLAGS.GUILD_MESSAGE_REACTIONS] });

client.on('ready', () => {
   console.log(`Logged in as ${client.user.tag}!`);
   client.user.setActivity("the market");
});

client.on('messageCreate', msg => {
   try {
      if (msg.author.bot || !msg.guild) return;
      if (msg.member.permissionsIn(msg.channel).has("ADMINISTRATOR")) {
         if (msg.content.startsWith("~link ") && msg.content.indexOf("<") != -1) {
            PassThrough;
         }
      }
      if (msg.content.startsWith("~test")) {
         msg.reply('grug is here');
      }
   }
   catch (e) {
      msg.reply(`UNCAUGHT ERROR: ${e}`);
   }
});

function updater() {
   updateBoards(client);
}


client.login(token);