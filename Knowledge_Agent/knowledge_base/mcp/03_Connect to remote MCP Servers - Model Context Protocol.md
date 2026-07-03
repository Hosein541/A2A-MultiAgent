> ## Documentation Index
>
> Fetch the complete documentation index at: [/llms.txt](https://modelcontextprotocol.io/llms.txt)
>
> Use this file to discover all available pages before exploring further.

[Skip to main content](https://modelcontextprotocol.io/docs/develop/connect-remote-servers#content-area)

Remote MCP servers extend AI applications’ capabilities beyond your local environment, providing access to internet-hosted tools, services, and data sources. By connecting to remote MCP servers, you transform AI assistants from helpful tools into informed teammates capable of handling complex, multi-step projects with real-time access to external resources.Many clients now support remote MCP servers, enabling a wide range of integration possibilities. This guide demonstrates how to connect to remote MCP servers using [Claude](https://claude.ai/) as an example, one of the many clients that support MCP. While we focus on Claude’s implementation through Custom Connectors, the concepts apply broadly to other MCP-compatible clients.

## [​](https://modelcontextprotocol.io/docs/develop/connect-remote-servers\#understanding-remote-mcp-servers)  Understanding Remote MCP Servers

Remote MCP servers function similarly to local MCP servers but are hosted on the internet rather than your local machine. They expose tools, prompts, and resources that Claude can use to perform tasks on your behalf. These servers can integrate with various services such as project management tools, documentation systems, code repositories, and any other API-enabled service.The key advantage of remote MCP servers is their accessibility. Unlike local servers that require installation and configuration on each device, remote servers are available from any MCP client with an internet connection. This makes them ideal for web-based AI applications, integrations that emphasize ease of use, and services that require server-side processing or authentication.

## [​](https://modelcontextprotocol.io/docs/develop/connect-remote-servers\#what-are-custom-connectors)  What are Custom Connectors?

Custom Connectors serve as the bridge between Claude and remote MCP servers. They allow you to connect Claude directly to the tools and data sources that matter most to your workflows, enabling Claude to operate within your favorite software and draw insights from the complete context of your external tools.With Custom Connectors, you can:

- [Connect Claude to existing remote MCP servers](https://support.anthropic.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp) provided by third-party developers
- [Build your own remote MCP servers to connect with any tool](https://support.anthropic.com/en/articles/11503834-building-custom-connectors-via-remote-mcp-servers)

## [​](https://modelcontextprotocol.io/docs/develop/connect-remote-servers\#connecting-to-a-remote-mcp-server)  Connecting to a Remote MCP Server

The process of connecting Claude to a remote MCP server involves adding a Custom Connector through the [Claude interface](https://claude.ai/). This establishes a secure connection between Claude and your chosen remote server.

1

[Navigate to header](https://modelcontextprotocol.io/docs/develop/connect-remote-servers#)

Navigate to Connector Settings

Open Claude in your browser and navigate to the settings page. You can access this by clicking on your profile icon and selecting “Settings” from the dropdown menu. Once in settings, locate and click on the “Connectors” section in the sidebar.This will display your currently configured connectors and provide options to add new ones.

2

[Navigate to header](https://modelcontextprotocol.io/docs/develop/connect-remote-servers#)

Add a Custom Connector

In the Connectors section, scroll to the bottom where you’ll find the “Add custom connector” button. Click this button to begin the connection process.

![Add custom connector button in Claude settings](https://mintcdn.com/mcp/4ZXF1PrDkEaJvXpn/images/quickstart-remote/1-add-connector.png?fit=max&auto=format&n=4ZXF1PrDkEaJvXpn&q=85&s=b5ae9b23164875bbaa3aff4c178cdc64)

A dialog will appear prompting you to enter the remote MCP server URL. This URL should be provided by the server developer or administrator. Enter the complete URL, ensuring it includes the proper protocol (https://) and any necessary path components.

![Dialog for entering remote MCP server URL](https://mintcdn.com/mcp/4ZXF1PrDkEaJvXpn/images/quickstart-remote/2-connect.png?fit=max&auto=format&n=4ZXF1PrDkEaJvXpn&q=85&s=0934f16d8e016cade8e560c8f89d011b)

After entering the URL, click “Add” to proceed with the connection.

3

[Navigate to header](https://modelcontextprotocol.io/docs/develop/connect-remote-servers#)

Complete Authentication

Most remote MCP servers require authentication to ensure secure access to their resources. The authentication process varies depending on the server implementation but commonly involves OAuth, API keys, or username/password combinations.

![Authentication screen for remote MCP server](https://mintcdn.com/mcp/4ZXF1PrDkEaJvXpn/images/quickstart-remote/3-auth.png?fit=max&auto=format&n=4ZXF1PrDkEaJvXpn&q=85&s=89af6e1b85718637231388697cc7b015)

Follow the authentication prompts provided by the server. This may redirect you to a third-party authentication provider or display a form within Claude. Once authentication is complete, Claude will establish a secure connection to the remote server.

4

[Navigate to header](https://modelcontextprotocol.io/docs/develop/connect-remote-servers#)

Access Resources and Prompts

After successful connection, the remote server’s resources and prompts become available in your Claude conversations. You can access these by clicking the paperclip icon in the message input area, which opens the attachment menu.

![Attachment menu showing available resources](https://mintcdn.com/mcp/4ZXF1PrDkEaJvXpn/images/quickstart-remote/4-select-resources-menu.png?fit=max&auto=format&n=4ZXF1PrDkEaJvXpn&q=85&s=ecc6234b0fe5625e24cc2b02b7893c67)

The menu displays all available resources and prompts from your connected servers. Select the items you want to include in your conversation. These resources provide Claude with context and information from your external tools.

![Selecting specific resources and prompts from the menu](https://mintcdn.com/mcp/4ZXF1PrDkEaJvXpn/images/quickstart-remote/5-select-prompts-resources.png?fit=max&auto=format&n=4ZXF1PrDkEaJvXpn&q=85&s=30c522540c7ff5abd8617d20b329eca2)

5

[Navigate to header](https://modelcontextprotocol.io/docs/develop/connect-remote-servers#)

Configure Tool Permissions

Remote MCP servers often expose multiple tools with varying capabilities. You can control which tools Claude is allowed to use by configuring permissions in the connector settings. This ensures Claude only performs actions you’ve explicitly authorized.

![Tool permission configuration interface](https://mintcdn.com/mcp/4ZXF1PrDkEaJvXpn/images/quickstart-remote/6-configure-tools.png?fit=max&auto=format&n=4ZXF1PrDkEaJvXpn&q=85&s=1e55fd2f7da85150bfcf9dfbd7a31f44)

Navigate back to the Connectors settings and click on your connected server. Here you can enable or disable specific tools, set usage limits, and configure other security parameters according to your needs.

## [​](https://modelcontextprotocol.io/docs/develop/connect-remote-servers\#best-practices-for-using-remote-mcp-servers)  Best Practices for Using Remote MCP Servers

When working with remote MCP servers, consider these recommendations to ensure a secure and efficient experience:**Security considerations**: Always verify the authenticity of remote MCP servers before connecting. Only connect to servers from trusted sources, and review the permissions requested during authentication. Be cautious about granting access to sensitive data or systems.**Managing multiple connectors**: You can connect to multiple remote MCP servers simultaneously. Organize your connectors by purpose or project to maintain clarity. Regularly review and remove connectors you no longer use to keep your workspace organized and secure.

## [​](https://modelcontextprotocol.io/docs/develop/connect-remote-servers\#next-steps)  Next Steps

Now that you’ve connected Claude to a remote MCP server, you can explore its capabilities in your conversations. Try using the connected tools to automate tasks, access external data, or integrate with your existing workflows.

[**Build your own remote server** \\
\\
Create custom remote MCP servers to integrate with proprietary tools and\\
services](https://support.anthropic.com/en/articles/11503834-building-custom-connectors-via-remote-mcp-servers)

[**Explore available servers** \\
\\
Browse our collection of official and community-created MCP servers](https://github.com/modelcontextprotocol/servers)

[**Connect local servers** \\
\\
Learn how to connect Claude Desktop to local MCP servers for direct system\\
access](https://modelcontextprotocol.io/docs/develop/connect-local-servers)

[**Understand the architecture** \\
\\
Dive deeper into how MCP works and its architecture](https://modelcontextprotocol.io/docs/learn/architecture)

Remote MCP servers unlock powerful possibilities for extending Claude’s capabilities. As you become familiar with these integrations, you’ll discover new ways to streamline your workflows and accomplish complex tasks more efficiently.

Was this page helpful?

YesNo

[Connect to local MCP servers](https://modelcontextprotocol.io/docs/develop/connect-local-servers) [Build with Agent Skills](https://modelcontextprotocol.io/docs/develop/build-with-agent-skills)

Ctrl+I

Assistant

Responses are generated using AI and may contain mistakes.

![Add custom connector button in Claude settings](https://mintcdn.com/mcp/4ZXF1PrDkEaJvXpn/images/quickstart-remote/1-add-connector.png?w=1100&fit=max&auto=format&n=4ZXF1PrDkEaJvXpn&q=85&s=c55cb3531701df2b5dfd721dcd3f48dc)

![Dialog for entering remote MCP server URL](https://mintcdn.com/mcp/4ZXF1PrDkEaJvXpn/images/quickstart-remote/2-connect.png?w=1100&fit=max&auto=format&n=4ZXF1PrDkEaJvXpn&q=85&s=15b6cd3819fabd3655a52b930d384b51)

![Authentication screen for remote MCP server](https://mintcdn.com/mcp/4ZXF1PrDkEaJvXpn/images/quickstart-remote/3-auth.png?w=1100&fit=max&auto=format&n=4ZXF1PrDkEaJvXpn&q=85&s=e78e71303fd5bb7d1e5c1602dca7641b)

![Attachment menu showing available resources](https://mintcdn.com/mcp/4ZXF1PrDkEaJvXpn/images/quickstart-remote/4-select-resources-menu.png?w=1100&fit=max&auto=format&n=4ZXF1PrDkEaJvXpn&q=85&s=00fc5842c2d6592f41f96c2051b016e2)

![Selecting specific resources and prompts from the menu](https://mintcdn.com/mcp/4ZXF1PrDkEaJvXpn/images/quickstart-remote/5-select-prompts-resources.png?w=1100&fit=max&auto=format&n=4ZXF1PrDkEaJvXpn&q=85&s=19d1f1de9b7b38dff6fabaea260fc700)

![Tool permission configuration interface](https://mintcdn.com/mcp/4ZXF1PrDkEaJvXpn/images/quickstart-remote/6-configure-tools.png?w=1100&fit=max&auto=format&n=4ZXF1PrDkEaJvXpn&q=85&s=8b7ea5b326ea5cf8947e9b9aba28f2f7)