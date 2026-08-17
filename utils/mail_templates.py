def base_email_template(title: str, content_html: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
      </head>

      <body
        style="
          margin: 0;
          padding: 0;
          background-color: #F7F5F0;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI',
            Roboto, Helvetica, Arial, sans-serif;
          color: #171717;
          -webkit-font-smoothing: antialiased;
        "
      >
        <table
          border="0"
          cellpadding="0"
          cellspacing="0"
          width="100%"
          style="background-color: #F7F5F0; padding: 40px 20px;"
        >
          <tr>
            <td align="center">

              <!-- Main Card -->
              <table
                border="0"
                cellpadding="0"
                cellspacing="0"
                width="100%"
                style="
                  max-width: 500px;
                  background-color: #FFFFFF;
                  border: 1px solid #E5E2DC;
                  border-radius: 8px;
                  overflow: hidden;
                  padding: 32px 24px;
                "
              >

                <!-- Header -->
                <tr>
                  <td
                    style="
                      padding-bottom: 24px;
                      border-bottom: 1px solid #E5E2DC;
                      text-align: left;
                    "
                  >
                    <span
                      style="
                        font-size: 20px;
                        font-weight: 700;
                        color: #171717;
                        letter-spacing: -0.5px;
                      "
                    >
                      Since
                    </span>
                  </td>
                </tr>

                <!-- Body -->
                <tr>
                  <td
                    style="
                      padding-top: 24px;
                      font-size: 14px;
                      line-height: 1.6;
                      color: #171717;
                    "
                  >
                    {content_html}
                  </td>
                </tr>

                <!-- Footer -->
                <tr>
                  <td
                    style="
                      padding-top: 32px;
                      border-top: 1px solid #E5E2DC;
                      margin-top: 32px;
                      text-align: center;
                      font-size: 12px;
                      color: #737373;
                    "
                  >
                    &copy; Since. All rights reserved.<br/>
                    If you didn't request this email, you can safely ignore it.
                  </td>
                </tr>

              </table>

            </td>
          </tr>
        </table>
      </body>
    </html>
    """


def get_button_html(url: str, text: str) -> str:
    return f"""
    <div style="margin: 28px 0; text-align: center;">
      <a
        href="{url}"
        target="_blank"
        style="
          background-color: #171717;
          color: #FFFFFF;
          text-decoration: none;
          padding: 12px 24px;
          border-radius: 6px;
          font-weight: 500;
          font-size: 14px;
          display: inline-block;
        "
      >
        {text}
      </a>
    </div>
    """


def get_signup_email(confirmation_url: str) -> str:
    content = f"""
    <h2
      style="
        margin: 0 0 16px 0;
        font-size: 20px;
        color: #171717;
        font-weight: 600;
      "
    >
      Confirm your email address
    </h2>

    <p
      style="
        margin: 0 0 16px 0;
        color: #737373;
      "
    >
      Welcome to Since! Please confirm your email address by clicking
      the button below.
    </p>

    {get_button_html(confirmation_url, "Confirm Email")}

    <p
      style="
        margin: 0;
        font-size: 12px;
        color: #737373;
      "
    >
      Or copy and paste this URL into your browser:<br/>
      <a
        href="{confirmation_url}"
        style="color: #171717;"
      >
        {confirmation_url}
      </a>
    </p>
    """

    return base_email_template("Confirm Your Email", content)


def get_signin_notification_email() -> str:
    content = """
    <h2
      style="
        margin: 0 0 16px 0;
        font-size: 20px;
        color: #171717;
        font-weight: 600;
      "
    >
      New Sign-In Detected
    </h2>

    <p
      style="
        margin: 0 0 16px 0;
        color: #737373;
      "
    >
      We noticed a new sign-in to your Since account.
      If this was you, no action is required.
    </p>

    <p
      style="
        margin: 0;
        font-size: 13px;
        color: #B85450;
        background-color: #FBF2F1;
        padding: 12px;
        border-radius: 6px;
        border-left: 3px solid #B85450;
      "
    >
      If you did not initiate this login, please reset your password
      immediately to secure your account.
    </p>
    """

    return base_email_template("New Login Alert", content)


def get_welcome_email() -> str:
    content = """
    <h2
      style="
        margin: 0 0 16px 0;
        font-size: 20px;
        color: #171717;
        font-weight: 600;
      "
    >
      Welcome to Since
    </h2>

    <p
      style="
        margin: 0 0 16px 0;
        color: #171717;
      "
    >
      Your email has been successfully verified,
      and your account is now fully active.
    </p>

    <p
      style="
        margin: 0;
        color: #737373;
      "
    >
      You can now start creating counters and tracking
      the things that matter to you.
    </p>
    """

    return base_email_template("Welcome to Since", content)


def get_forgot_password_email(reset_url: str) -> str:
    content = f"""
    <h2
      style="
        margin: 0 0 16px 0;
        font-size: 20px;
        color: #171717;
        font-weight: 600;
      "
    >
      Reset your password
    </h2>

    <p
      style="
        margin: 0 0 16px 0;
        color: #737373;
      "
    >
      We received a request to reset your Since account password.
      Click the button below to choose a new password.
    </p>

    {get_button_html(reset_url, "Reset Password")}

    <p
      style="
        margin: 0;
        font-size: 12px;
        color: #737373;
      "
    >
      This link is time-sensitive. If you did not request a password
      reset, you can safely ignore this email.
    </p>
    """

    return base_email_template("Reset Password", content)


def get_password_changed_email() -> str:
    content = """
    <h2
      style="
        margin: 0 0 16px 0;
        font-size: 20px;
        color: #171717;
        font-weight: 600;
      "
    >
      Password Changed
    </h2>

    <p
      style="
        margin: 0 0 16px 0;
        color: #171717;
      "
    >
      Your password for Since was successfully updated.
    </p>

    <p
      style="
        margin: 0;
        font-size: 13px;
        color: #B85450;
        background-color: #FBF2F1;
        padding: 12px;
        border-radius: 6px;
        border-left: 3px solid #B85450;
      "
    >
      If you did not perform this change, please contact support
      immediately.
    </p>
    """

    return base_email_template("Password Changed", content)
