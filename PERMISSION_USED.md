# Meta OAuth Permissions Used

This document outlines the permissions (OAuth scopes) requested during the Facebook and Instagram connect flow and their respective purposes in the application.

## Facebook Page Scopes

1. **`pages_show_list`**
   - **Purpose:** Allows the application to fetch the list of Facebook Pages that the user manages, so they can be displayed and selected for connection.

2. **`pages_messaging`**
   - **Purpose:** Required to read incoming Messenger messages and send automated replies via the chatbot backend.

3. **`pages_read_engagement`**
   - **Purpose:** Allows the app to read content (like posts and comments) from the Facebook Page, needed to monitor incoming engagements.

4. **`pages_manage_posts`**
   - **Purpose:** Enables the application to create, edit, or delete posts on behalf of the connected Facebook Page.

5. **`ads_management`**
   - **Purpose:** Grants the ability to create, read, and manage ads on behalf of the connected account (requested for "create ads and manage everything").

6. **`public_profile`**
   - **Purpose:** A basic permission to read the user's public profile, ensuring the app can associate the token with the correct Meta identity.

## Instagram Scopes

1. **`instagram_basic`**
   - **Purpose:** Allows the application to read basic information about the connected Instagram Professional account (like profile details and connected media).

2. **`instagram_manage_messages`**
   - **Purpose:** Required to read incoming Direct Messages on Instagram and send automated chat replies.

3. **`instagram_manage_comments`**
   - **Purpose:** Enables the app to read incoming comments on Instagram posts and automatically reply or hide them.

4. **`instagram_content_publish`**
   - **Purpose:** Allows the application to create and publish posts directly to the connected Instagram Professional account.

## Long-Lived Token Exchange
In addition to the above permissions, the backend performs a token exchange using `grant_type=fb_exchange_token` to convert the short-lived user access token obtained in the browser into a **long-lived** token (usually valid for 60 days). Using this long-lived user token to request page access tokens generates **permanent page access tokens** that do not expire, allowing the application to function continuously without requiring the user to frequently re-authenticate.
