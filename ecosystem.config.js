module.exports = {
  apps: [{
    name: 'AndromuxBOT',
    script: 'bot.py',
    interpreter: '/home/miguel/workspace/discord_bot/.venv/bin/python3',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '200M',
    env: {
      NODE_ENV: 'development'
    },
    env_production: {
      NODE_ENV: 'production'
    },
    error_file: './logs/err.log',
    out_file: './logs/out.log',
    log_file: './logs/combined.log',
    time: true
  }]
};
