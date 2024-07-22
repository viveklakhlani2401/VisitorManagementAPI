import os
def email_template(email, message, otp):
    email_body = f"""
<html>
    <head>
        <title>Aawjo</title>
        <style type="text/css">
            #outlook a {{ padding: 0; }}
            body {{
                margin: 0;
                padding: 0;
                -webkit-text-size-adjust: 100%;
                -ms-text-size-adjust: 100%;
                background-color: #FCFAFF;
                display: flex;
                justify-content: center;
                height: 100vh;
                align-items: center;
            }}
            table, td {{ border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; }}
            p {{ display: block; margin: 13px 0; }}
        </style>
        <link href="https://fonts.googleapis.com/css?family=Inter:400,700" rel="stylesheet" type="text/css">
    </head>
    <body>
        <div style="display:none;font-size:1px;color:#ffffff;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">
            Automatic email sent by Aawjo. Please, don&#x27;t reply.
        </div>
        <div style="background-color:#FCFAFF;">
            <div class="body-section" style="-webkit-box-shadow: 0 1px 3px 0 rgba(0, 20, 32, 0.12); -moz-box-shadow: 0 1px 3px 0 rgba(0, 20, 32, 0.12); box-shadow: 0 1px 3px 0 rgba(0, 20, 32, 0.12); margin: 0px auto; max-width: 460px;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
                    <tbody>
                        <tr>
                            <td style="direction:ltr;font-size:0px;padding:0px;text-align:center;">
                                <div style="background:#FFFFFF;background-color:#FFFFFF;margin:0px auto;border-radius:8px;max-width:460px;">
                                    <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#FFFFFF;background-color:#FFFFFF;width:100%;border-radius:8px;margin-top: 4rem;">
                                        <tbody>
                                            <tr>
                                                <td style="direction:ltr;font-size:0px;padding:20px 0;padding-bottom:25px;padding-left:10px;padding-right:10px;padding-top:25px;text-align:center;">
                                                    <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                                                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                                                            <tr>
                                                                <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                                                                    <div style="font-family:Inter, Helvetica, Arial, sans-serif;font-size:18px;font-weight:500;line-height:36px;text-align:left;color:#1D3344;">
                                                                        Hi {email.split("@")[0]},
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                            <tr>
                                                                <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                                                                    <div style="font-family:Inter, Helvetica, Arial, sans-serif;font-size:14px;font-weight:400;line-height:21px;text-align:left;color:#001420;">
                                                                        {message}
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                            <tr>
                                                                <td style="display: flex; font-size:0px;padding:20px 0;padding-top:10px;padding-right:25px;padding-bottom:10px;padding-left:25px;word-break:break-word;">
                                                                    <div style="display: flex;justify-content: center;margin:0px auto;max-width:440px;">
                                                                        <p style="margin:0;padding:0;padding-bottom:20px;line-height:1.6;font-family:'Inter';color:#2d4f43;font-family:'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;font-weight: 600;font-size:24px;text-align: center;">
                                                                            {otp}
                                                                        </p>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                            <tr>
                                                                <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                                                                    <div style="font-family:Inter, Helvetica, Arial, sans-serif;font-size:14px;font-weight:400;line-height:21px;text-align:left;color:#001420;">
                                                                        OTP is valid for 5 minutes.
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </div>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div style="margin:0px auto;max-width:460px;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
                    <tbody>
                        <tr>
                            <td style="direction:ltr;font-size:0px;padding:20px 0;padding-top:8px;text-align:center;">
                                <div style="background:#FCFAFF;background-color:#FCFAFF;margin:0px auto;max-width:460px;">
                                    <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#FCFAFF;background-color:#FCFAFF;width:100%;">
                                        <tbody>
                                            <tr>
                                                <td style="direction:ltr;font-size:0px;padding:20px 0;padding-bottom:25px;padding-left:10px;padding-right:10px;padding-top:25px;text-align:center;">
                                                    <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                                                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                                                            <tr>
                                                                <td align="center" style="font-size:0px;padding:10px 25px;padding-top:0px;word-break:break-word;">
                                                                    <div style="font-family:Inter, Helvetica, Arial, sans-serif;font-size:12px;font-weight:400;line-height:16px;text-align:center;color:#5B768C;">
                                                                        The email is auto-generated. Please, don&#x27;t reply.
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </div>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </body>
</html>
"""
    return email_body


def send_credential_email(fname,username,password):
    email_body = f"""
<html>

<head>
    <title>Aawjo</title>
    <style type="text/css">
        #outlook a {{
            padding: 0;
        }}

        body {{
            margin: 0;
            padding: 0;
            -webkit-text-size-adjust: 100%;
            -ms-text-size-adjust: 100%;
            background-color: #FCFAFF;
            display: flex;
            justify-content: center;
            height: 100vh;
            align-items: center;
        }}

        table,
        td {{
            border-collapse: collapse;
            mso-table-lspace: 0pt;
            mso-table-rspace: 0pt;
        }}

        p {{
            display: block;
            margin: 13px 0;
        }}
    </style>
    <link href="https://fonts.googleapis.com/css?family=Inter:400,700" rel="stylesheet" type="text/css">
</head>

<body>
    <div
        style="display:none;font-size:1px;color:#ffffff;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">
        Automatic email sent by Aawjo. Please, don&#x27;t reply.
    </div>
    <div style="background-color:#FCFAFF;">
        <div class="body-section">
            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%">
                <tbody>
                    <tr>
                        <td style="direction:ltr;font-size:0px;padding:0px;text-align:center">
                            <div
                                style="background:#ffffff;background-color:#ffffff;margin:41px auto;border-radius:8px;max-width:460px">
                                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
                                    style="background:#ffffff;background-color:#ffffff;width:100%;border-radius:8px">
                                    <tbody>
                                        <tr>
                                            <td
                                                style="direction:ltr;font-size:0px;padding:20px 0;padding-bottom:25px;padding-left:10px;padding-right:10px;padding-top:25px;text-align:center">
                                                <div
                                                    style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%">
                                                    <table border="0" cellpadding="0" cellspacing="0"
                                                        role="presentation" style="vertical-align:top" width="100%">
                                                        <tbody>
                                                            <tr>
                                                                <td align="left"
                                                                    style="font-size:0px;padding:10px 25px;word-break:break-word">
                                                                    <div
                                                                        style="font-family:Montserrat,Helvetica,Arial,sans-serif;font-size:30px;font-weight:700;line-height:36px;text-align:left;color:#1d3344">
                                                                        Hi {fname},</div>
                                                                </td>
                                                            </tr>
                                                            <tr>
                                                                <td align="left"
                                                                    style="font-size:0px;padding:10px 25px;word-break:break-word">
                                                                    <div
                                                                        style="font-family:Montserrat,Helvetica,Arial,sans-serif;font-size:14px;font-weight:500;line-height:21px;text-align:left;color:#001420">
                                                                        Your Aawjo account password has been updated by
                                                                        the manager. </div>
                                                                </td>
                                                            </tr>
                                                            <tr>
                                                                <td align="left"
                                                                    style="font-size:0px;padding:10px 25px;word-break:break-word">
                                                                    <div
                                                                        style="font-family:Montserrat,Helvetica,Arial,sans-serif;font-size:13px;font-weight:400;line-height:21px;text-align:left;color:#001420">
                                                                        Please find your credentials below.</div>
                                                                </td>
                                                            </tr>
                                                            <tr>
                                                                <td
                                                                    style="font-size:0px;padding:20px 0;padding-top:10px;padding-right:25px;padding-bottom:10px;padding-left:25px;word-break:break-word">
                                                                    <div
                                                                        style="background:#FCFAFF;background-color:#FCFAFF;margin:0px auto;max-width:440px">
                                                                        <table align="center" border="0" cellpadding="0"
                                                                            cellspacing="0" role="presentation"
                                                                            style="background:#FCFAFF;background-color:#FCFAFF;width:100%">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td
                                                                                        style="border-left:4px solid #7F56D9;direction:ltr;font-size:0px;padding:20px 0;padding-bottom:10px;padding-left:25px;padding-right:25px;padding-top:10px;text-align:center">
                                                                                        <div
                                                                                            style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%">
                                                                                            <table border="0"
                                                                                                cellpadding="0"
                                                                                                cellspacing="0"
                                                                                                role="presentation"
                                                                                                style="vertical-align:top"
                                                                                                width="100%">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td align="left"
                                                                                                            style="font-size:0px;padding:0px;word-break:break-word">
                                                                                                            <div
                                                                                                                style="font-family:Montserrat,Helvetica,Arial,sans-serif;font-size:12px;font-weight:400;line-height:16px;text-align:left;color:#5b768c">

                                                                                                                Username:
                                                                                                            </div>
                                                                                                        </td>
                                                                                                    </tr>
                                                                                                    <tr>
                                                                                                        <td align="left"
                                                                                                            style="font-size:0px;padding:0px;word-break:break-word">
                                                                                                            <div
                                                                                                                style="font-family:Montserrat,Helvetica,Arial,sans-serif;font-size:14px;font-weight:700;line-height:21px;text-align:left;color:#001420">
                                                                                                                {username}
                                                                                                            </div>
                                                                                                        </td>
                                                                                                    </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                        </div>

                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                            <tr>
                                                                <td
                                                                    style="font-size:0px;padding:20px 0;padding-top:10px;padding-right:25px;padding-bottom:10px;padding-left:25px;word-break:break-word">
                                                                    <div
                                                                        style="background:#FCFAFF;background-color:#FCFAFF;margin:0px auto;max-width:440px">
                                                                        <table align="center" border="0" cellpadding="0"
                                                                            cellspacing="0" role="presentation"
                                                                            style="background:#FCFAFF;background-color:#FCFAFF;width:100%">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td
                                                                                        style="border-left:4px solid #7F56D9;direction:ltr;font-size:0px;padding:20px 0;padding-bottom:10px;padding-left:25px;padding-right:25px;padding-top:10px;text-align:center">
                                                                                        <div
                                                                                            style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%">
                                                                                            <table border="0"
                                                                                                cellpadding="0"
                                                                                                cellspacing="0"
                                                                                                role="presentation"
                                                                                                style="vertical-align:top"
                                                                                                width="100%">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td align="left"
                                                                                                            style="font-size:0px;padding:0px;word-break:break-word">
                                                                                                            <div
                                                                                                                style="font-family:Montserrat,Helvetica,Arial,sans-serif;font-size:12px;font-weight:400;line-height:16px;text-align:left;color:#5b768c">

                                                                                                                Password:
                                                                                                            </div>
                                                                                                        </td>
                                                                                                    </tr>
                                                                                                    <tr>
                                                                                                        <td align="left"
                                                                                                            style="font-size:0px;padding:0px;word-break:break-word">
                                                                                                            <div
                                                                                                                style="font-family:Montserrat,Helvetica,Arial,sans-serif;font-size:14px;font-weight:700;line-height:21px;text-align:left;color:#001420">
                                                                                                                {password}
                                                                                                            </div>
                                                                                                        </td>
                                                                                                    </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                        </div>

                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                            <tr>
                                                                <td align="center"
                                                                    style="font-size:0px;padding:10px 25px;word-break:break-word">
                                                                    <table border="0" cellpadding="0" cellspacing="0"
                                                                        role="presentation"
                                                                        style="border-collapse:separate;width:200px;line-height:100%">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td align="center" bgcolor="#7F56D9"
                                                                                    role="presentation"
                                                                                    style="border:none;border-radius:8px;background:#7F56D9"
                                                                                    valign="middle"><a
                                                                                        href="{os.getenv("FRONTEND_URL")}"
                                                                                        style="display:inline-block;width:150px;background:#7F56D9;color:#ffffff;font-family:Montserrat,Helvetica,Arial,sans-serif;font-size:14px;font-weight:400;line-height:21px;margin:0;text-decoration:none;text-transform:none;padding:10px 25px;border-radius:8px"
                                                                                        target="_blank">Sign
                                                                                        In</a></td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                            </tr>

                                                            <tr>
                                                                <td align="left"
                                                                    style="font-size:0px;padding:10px 25px;word-break:break-word">
                                                                    <div
                                                                        style="font-family:Montserrat,Helvetica,Arial,sans-serif;font-size:13px;font-weight:400;line-height:21px;text-align:left;color:#001420">
                                                                        Thank you,<br /><span
                                                                            style="font-family:Montserrat,Helvetica,Arial,sans-serif;font-size:14px;font-weight:500;line-height:21px;text-align:left;color:#001420">

                                                                            Aawjo team
                                                                        </span>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                </div>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div style="margin:0px auto;max-width:460px;">
            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
                <tbody>
                    <tr>
                        <td style="direction:ltr;font-size:0px;padding:20px 0;padding-top:8px;text-align:center;">
                            <div style="background:#FCFAFF;background-color:#FCFAFF;margin:0px auto;max-width:460px;">
                                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
                                    style="background:#FCFAFF;background-color:#FCFAFF;width:100%;">
                                    <tbody>
                                        <tr>
                                            <td
                                                style="direction:ltr;font-size:0px;padding:20px 0;padding-bottom:25px;padding-left:10px;padding-right:10px;padding-top:25px;text-align:center;">
                                                <div class="mj-column-per-100 mj-outlook-group-fix"
                                                    style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                                                    <table border="0" cellpadding="0" cellspacing="0"
                                                        role="presentation" style="vertical-align:top;" width="100%">
                                                        <tr>
                                                            <td align="center"
                                                                style="font-size:0px;padding:10px 25px;padding-top:0px;word-break:break-word;">
                                                                <div
                                                                    style="font-family:Inter, Helvetica, Arial, sans-serif;font-size:12px;font-weight:400;line-height:16px;text-align:center;color:#5B768C;">
                                                                    The email is auto-generated. Please, don&#x27;t
                                                                    reply.
                                                                </div>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </div>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</body>

</html>
"""
    return email_body

def send_reminder(visitor,message,link,text,linktext):
    email_body = f"""
<html>

<head>
    <title>Aawjo</title>
    <style type="text/css">
        #outlook a {{
            padding: 0;
        }}

        body {{
            margin: 0;
            padding: 0;
            -webkit-text-size-adjust: 100%;
            -ms-text-size-adjust: 100%;
            background-color: #FCFAFF;
            display: flex;
            justify-content: center;
            height: 100vh;
            align-items: center;
        }}

        table,
        td {{
            border-collapse: collapse;
            mso-table-lspace: 0pt;
            mso-table-rspace: 0pt;
        }}

        p {{
            display: block;
            margin: 13px 0;
        }}
    </style>
    <link href="https://fonts.googleapis.com/css?family=Inter:400,700" rel="stylesheet" type="text/css">
</head>

<body>
    <div
        style="display:none;font-size:1px;color:#ffffff;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">
        Automatic email sent by Aawjo. Please, don&#x27;t reply.
    </div>
    <div style="background-color:#FCFAFF;">
        <div class="body-section">
            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%">
                <tbody>
                    <tr>
                        <td style="direction:ltr;font-size:0px;padding:0px;text-align:center">
                            <div
                                style="background:#ffffff;background-color:#ffffff;margin:41px auto;border-radius:8px;max-width:460px">
                                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
                                    style="background:#ffffff;background-color:#ffffff;width:100%;border-radius:8px">
                                    <tbody>
                                        <tr>
                                            <td
                                                style="direction:ltr;font-size:0px;padding:20px 0;padding-bottom:25px;padding-left:10px;padding-right:10px;padding-top:25px;text-align:center">
                                                <div
                                                    style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%">
                                                    <table border="0" cellpadding="0" cellspacing="0"
                                                        role="presentation" style="vertical-align:top" width="100%">
                                                        <tbody>
                                                            <tr>
                                                                <td align="left"
                                                                    style="font-size:0px;padding:10px 25px;word-break:break-word">
                                                                    <div
                                                                        style="font-family:Montserrat,Helvetica,Arial,sans-serif;font-size:30px;font-weight:700;line-height:36px;text-align:left;color:#1d3344">
                                                                        Hi {visitor['vName']},</div>
                                                                </td>
                                                            </tr>
                                                            <tr>
                                                                <td align="left"
                                                                    style="font-size:0px;padding:10px 25px;word-break:break-word">
                                                                    <div
                                                                        style="font-family:Montserrat,Helvetica,Arial,sans-serif;font-size:14px;font-weight:500;line-height:21px;text-align:left;color:#001420">
                                                                        {message}</div>
                                                                </td>
                                                            </tr>
                                                            <tr>
                                                                <td align="left"
                                                                    style="font-size:0px;padding:10px 25px;word-break:break-word">
                                                                    <div
                                                                        style="font-family:Montserrat,Helvetica,Arial,sans-serif;font-size:13px;font-weight:400;line-height:21px;text-align:left;color:#001420">

                                                                        <h3>Visit Schedule:</h3>
                                                                        <div class="details">
                                                                            <p><strong>Date and Time:</strong> {visitor['timeslot']}</p>
                                                                            <p><strong>Location:</strong> {visitor['vLocation']}</p>
                                                                        </div>
                                                                        <p>{text}</strong>.</p>
                                                                        <a href={link} class="button">{linktext}</a>
                                                                    </div>
                                                                </td>
                                                            </tr>


                                                            <tr>
                                                                <td align="left"
                                                                    style="font-size:0px;padding:10px 25px;word-break:break-word">
                                                                    <div
                                                                        style="font-family:Montserrat,Helvetica,Arial,sans-serif;font-size:13px;font-weight:400;line-height:21px;text-align:left;color:#001420">
                                                                        Thank you,<br /><span
                                                                            style="font-family:Montserrat,Helvetica,Arial,sans-serif;font-size:14px;font-weight:500;line-height:21px;text-align:left;color:#001420">

                                                                            Aawjo team
                                                                        </span>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                </div>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div style="margin:0px auto;max-width:460px;">
            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
                <tbody>
                    <tr>
                        <td style="direction:ltr;font-size:0px;padding:20px 0;padding-top:8px;text-align:center;">
                            <div style="background:#FCFAFF;background-color:#FCFAFF;margin:0px auto;max-width:460px;">
                                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
                                    style="background:#FCFAFF;background-color:#FCFAFF;width:100%;">
                                    <tbody>
                                        <tr>
                                            <td
                                                style="direction:ltr;font-size:0px;padding:20px 0;padding-bottom:25px;padding-left:10px;padding-right:10px;padding-top:25px;text-align:center;">
                                                <div class="mj-column-per-100 mj-outlook-group-fix"
                                                    style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                                                    <table border="0" cellpadding="0" cellspacing="0"
                                                        role="presentation" style="vertical-align:top;" width="100%">
                                                        <tr>
                                                            <td align="center"
                                                                style="font-size:0px;padding:10px 25px;padding-top:0px;word-break:break-word;">
                                                                <div
                                                                    style="font-family:Inter, Helvetica, Arial, sans-serif;font-size:12px;font-weight:400;line-height:16px;text-align:center;color:#5B768C;">
                                                                    The email is auto-generated. Please, don&#x27;t
                                                                    reply.
                                                                </div>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </div>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</body>

</html>
"""
    return email_body