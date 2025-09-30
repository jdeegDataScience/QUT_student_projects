[
    {
        endpoint: ".../user/register",
        body: { "email": "test2@email.com",
            "password": "pass" }
    },
    {
        endpoint: ".../user/login",
        body: { "email": "test2@email.com",
            "password": "pass" }
    },
    {
        endpoint: ".../user/refresh",
        body: { "refreshToken": "eyJ...CJ9.eyJ...cxfQ.q_a...BLs" }
    },
    {
        endpoint: ".../videos",
        auth: { BearerToken: "eyJ...CJ9.eyJ...cxfQ.q_a...BLs" }
    },
    {
        endpoint: ".../videos/convert",
        auth: { BearerToken: "eyJ...CJ9.eyJ...cxfQ.q_a...BLs" },
        body: 
        {
            video: 
            {
                url: "https://www.youtube.com/watch?v=a4na2opArGY",
                title: "DanDaDan S1 Opening",
                thumbnail: "https://i.ytimg.com/vi/a4na2opArGY/hqdefault.jpg?sqp=-oaymwEnCPYBEIoBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLD0SvSiNDRp-CRlmoObwUb8mIrdbA",
                length: 101
            }
        }
    }
]