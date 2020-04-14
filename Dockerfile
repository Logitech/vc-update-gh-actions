FROM node:slim

# Labels for GitHub to read your action
LABEL "com.github.actions.name"="GitHub checks updater"
LABEL "com.github.actions.description"="Marks all previously executed check runs for a given commit ref as successful"
LABEL "com.github.actions.icon"="book-open"
LABEL "com.github.actions.color"="blue"

# Copy the package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy the rest of your action's code
COPY . .

# Run `node /index.js`
ENTRYPOINT ["node", "/index.js"]
