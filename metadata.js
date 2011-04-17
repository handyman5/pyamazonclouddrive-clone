window.fwcim = new (function ()
{
    var g = "2.2.0";
    var O;
    var i;
    var a = [];
    var b;
    var N;
    var e;
    var x;
    var l;
    var G;
    var K;
    var f;
    var D;
    var v = [];
    var y;
    var s;
    var J = [4169969034];
    var I = [];
    function o(S)
    {
        return S.replace(/\\/g, "\\\\").replace(/"/g, '\\"').replace(/[\r\n]/g, "");
    }
    function C(T, S)
    {
        message = S.message && ((S.name || "Error") + ": " + S.message) || S.toString();
        v.push("[" + T + "] " + o(message));
    }
    function R()
    {
        return navigator.userAgent.match(/Windows/i);
    }
    function n()
    {
        return navigator.userAgent.match(/MSIE [0-9.]+/i);
    }
    function w(T)
    {
        var Y = ["signin", "sign-in", "sign_in", "signInForm", "signInLeftForm", "signInRightForm", "signInMainForm", 
        "newAccountForm", "forgotPasswordForm", "changeAccountInformationForm"];
        var X = /^ap_.+_form$/;
        function S(aa, ab)
        {
            if ((aa.id == ab) || (aa.name == ab)) {
                K = aa;
                return true;
            }
            return false;
        }
        try
        {
            if ((typeof (T) == "string") && (T != "")) {
                for (var W in document.forms) {
                    if (S(document.forms[W], T)) {
                        return true;
                    }
                }
            }
            for (var W in document.forms)
            {
                var V = document.forms[W];
                for (var Z in Y) {
                    if (S(V, Y[Z])) {
                        return true;
                    }
                }
                if (V.id && V.id.match(X)) {
                    K = V;
                    return true;
                }
            }
        }
        catch (U) {
            C("lF", U);
        }
        return false;
    }
    function t()
    {
        try
        {
            if (!D) {
                throw new Error("No container");
            }
            var T = document.createElement("span");
            T.id = "fwcim-caps";
            T.style.behavior = "url('#default#clientCaps')";
            D.appendChild(T);
            return T;
        }
        catch (S) {
            C("pBC", S);
        }
        return null;
    }
    function k()
    {
        var U = 'Function dAXP(n, v)\non error resume next\nset o = CreateObject(v)\nIf IsObject(o) Then\nSelect case n\ncase "ShockwaveDirector"\nf = o.ShockwaveVersion("")\ncase "ShockwaveFlash"\nf = o.FlashVersion()\ncase "RealPlayer"\nf = o.GetVersionInfo\ncase Else\nf = ""\nend Select\ndAXP = f\nEnd If\nEnd Function';
        try
        {
            if (!D) {
                throw new Error("No container");
            }
            var S = document.createElement("script");
            S.type = "text/vbscript";
            S.text = U;
            D.appendChild(S);
        }
        catch (T) {
            C("pPVB", T);
        }
    }
    function p()
    {
        if (!navigator.plugins || (navigator.plugins.length < 1)) {
            return;
        }
        try
        {
            var W = navigator.plugins.length;
            for (var T = 0; T < W; T++)
            {
                var V = navigator.plugins[T];
                var X = V.name + " " + V.description.replace(/[^0-9]/g, "");
                a.push({
                    name : V.name, version : V.version, str : X
                });
                if (V.name.match(/Shockwave Flash/))
                {
                    if (V.version) {
                        l = V.version;
                    }
                    else {
                        var S = V.description.match(/([0-9.]+)\s+r([0-9.]+)/);
                        l = S && (S[1] + "." + S[2]);
                    }
                }
            }
        }
        catch (U) {
            C("dNP", U);
        }
    }
    function j()
    {
        var T = navigator.userAgent.match(/Windows NT 6.0/);
        k();
        function V(X, Z)
        {
            var W = dAXP(X, Z);
            if (W) {
                var Y = {
                    name : X, version : W, str : X + " : " + W
                };
                a.push(Y);
                return Y;
            }
            return null;
        }
        try
        {
            V("ShockwaveDirector", "SWCtl.SWCtl");
            var S = V("ShockwaveFlash", "ShockwaveFlash.ShockwaveFlash");
            if (S) {
                l = (S.version >> 16) + "." + (S.version & 65535);
            }
            if (!T)
            {
                V("RealPlayer", "RealPlayer.RealPlayer(tm) ActiveX Control (32-bit)");
                V("RealPlayer", "RealVideo.RealVideo(tm) ActiveX Control (32-bit)");
            }
        }
        catch (U) {
            C("dAXP", U);
        }
    }
    function H()
    {
        var W = 
        {
            AB : "{7790769C-0471-11D2-AF11-00C04FA35D02}", WDUN : "{89820200-ECBD-11CF-8B85-00AA005B4340}", 
            DA : "{283807B5-2C60-11D0-A31D-00AA00B92C03}", DAJC : "{4F216970-C90C-11D1-B5C7-0000F8051515}", 
            DS : "{44BBA848-CC51-11CF-AAFA-00AA00B6015C}", DHDB : "{9381D8F2-0288-11D0-9501-00AA00B911A5}", 
            DHDBFJ : "{4F216970-C90C-11D1-B5C7-0000F8051515}", ICW : "{5A8D6EE0-3E18-11D0-821E-444553540000}", 
            IE : "{89820200-ECBD-11CF-8B85-00AA005B4383}", IECFJ : "{08B0E5C0-4FCB-11CF-AAA5-00401C608555}", 
            WMP : "{22D6F312-B0F6-11D0-94AB-0080C74C7E95}", NN : "{44BBA842-CC51-11CF-AAFA-00AA00B6015B}", 
            OBP : "{3AF36230-A269-11D1-B5BF-0000F8051515}", OE : "{44BBA840-CC51-11CF-AAFA-00AA00B6015C}", 
            TS : "{CC2A9BA0-3BDD-11D0-821E-444553540000}", MVM : "{08B0E5C0-4FCB-11CF-AAA5-00401C608500}", 
            DDE : "{44BBA855-CC51-11CF-AAFA-00AA00B6015F}", DOTNET : "{6FAB99D0-BAB8-11D1-994A-00C04F98BBC9}", 
            YHOO : "{E5D12C4E-7B4F-11D3-B5C9-0050045C3C96}", SWDNEW : "{166B1BCA-3F9C-11CF-8075-444553540000}", 
            DOTNETFM : "{89B4C1CD-B018-4511-B0A1-5476DBF70820}", MDFH : "{8EFA4753-7169-4CC3-A28B-0A1643B8A39B}", 
            FLH : "{D27CDB6E-AE6D-11CF-96B8-444553540000}", SW : "{2A202491-F00D-11CF-87CC-0020AFEECF20}", 
            SWD : "{233C1507-6A77-46A4-9443-F871F945D258}", RP : "{CFCDAA03-8BE4-11CF-B84B-0020AFBBCCFA}", 
            QT : "{DE4AF3B0-F4D4-11D3-B41A-0050DA2E6C21}"
        };
        var V = t();
        try
        {
            if (!V) {
                return;
            }
            for (var X in W)
            {
                var T = W[X];
                if (V.isComponentInstalled(T, "componentid"))
                {
                    var S = V.getComponentVersion(T, "componentid");
                    a.push({
                        name : X, version : S, str : "|" + X + " " + S
                    });
                }
            }
        }
        catch (U) {
            C("dASC", U);
        }
    }
    function L()
    {
        try
        {
            b = screen.width + "-" + screen.height + "-" + screen.availHeight + "-" + screen.colorDepth;
            b += "-" + ((typeof (screen.deviceXDPI) != "undefined") ? screen.deviceXDPI : "*");
            b += "-" + ((typeof (screen.logicalXDPI) != "undefined") ? screen.logicalXDPI : "*");
            b += "-" + ((typeof (screen.fontSmoothingEnabled) != "undefined") ? (screen.fontSmoothingEnabled ? 1 : 0) : "*");
        }
        catch (S) {
            C("dS", S);
        }
    }
    function M()
    {
        try
        {
            var S = new Date();
            var T = new Date(S.getFullYear(), 0, 10);
            var V = new Date(T.toGMTString().replace(/ (GMT|UTC)/, ""));
            e = (V - T) / 3600000;
        }
        catch (U) {
            C("dTZ", U);
        }
    }
    function z(T)
    {
        var S = [];
        for (var U = 0; U < T.length; U++)
        {
            var V = T.charCodeAt(U);
            if (V < 128) {
                S.push(String.fromCharCode(V));
            }
            else
            {
                if ((V >= 128) && (V < 2048)) {
                    S.push(String.fromCharCode((V >> 6) | 192));
                    S.push(String.fromCharCode((V & 63) | 128));
                }
                else
                {
                    S.push(String.fromCharCode((V >> 12) | 224));
                    S.push(String.fromCharCode(((V >> 6) & 63) | 128));
                    S.push(String.fromCharCode((V & 63) | 128));
                }
            }
        }
        return S.join("");
    }
    function m(ac)
    {
        var S = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
        var T = [];
        var X, V, U, ab, aa, Z, Y;
        var W = 0;
        while (W < ac.length)
        {
            X = ac.charCodeAt(W++);
            V = ac.charCodeAt(W++);
            U = ac.charCodeAt(W++);
            ab = X >> 2;
            aa = ((X & 3) << 4) | (V >> 4);
            Z = ((V & 15) << 2) | (U >> 6);
            Y = U & 63;
            if (isNaN(V)) {
                Z = Y = 64;
            }
            else {
                if (isNaN(U)) {
                    Y = 64;
                }
            }
            T.push(S.charAt(ab));
            T.push(S.charAt(aa));
            T.push(S.charAt(Z));
            T.push(S.charAt(Y));
        }
        return T.join("");
    }
    J.push(4087877101);
    function r(ab)
    {
        if (ab.length == 0) {
            return "";
        }
        var V = J;
        var U = Math.ceil(ab.length / 4);
        var ad = [];
        for (var W = 0; W < U; W++)
        {
            ad[W] = (ab.charCodeAt(W * 4) & 255) + ((ab.charCodeAt(W * 4 + 1) & 255) << 8) + ((ab.charCodeAt(W * 4 + 2) & 255) << 16) + ((ab.charCodeAt(W * 4 + 3) & 255) << 24);
        }
        var ac = 2654435769;
        var ae = Math.floor(6 + 52 / U);
        var aa = ad[0];
        var Z = ad[U - 1];
        var X = 0;
        while (ae--> 0)
        {
            X += ac;
            var Y = (X >>> 2) & 3;
            for (var S = 0; S < U; S++)
            {
                aa = ad[(S + 1) % U];
                Z = ad[S] += (((Z >>> 5)^(aa << 2)) + ((aa >>> 3)^(Z << 4)))^((X^aa) + (V[(S & 3)^Y]^Z));
            }
        }
        var T = [];
        for (var W = 0; W < U; W++)
        {
            T[W] = String.fromCharCode((ad[W]) & 255, (ad[W] >>> 8) & 255, (ad[W] >>> 16) & 255, (ad[W] >>> 24) & 255);
        }
        return T.join("");
    }
    function c(U)
    {
        if (I.length == 0)
        {
            var T = 3988292384;
            for (var X = 0; X < 256; X++) {
                var W = X;
                for (var V = 0; V < 8; V++) {
                    if (W & 1 == 1) {
                        W = (W >>> 1)^T;
                    }
                    else {
                        W = (W >>> 1);
                    }
                }
                I[X] = W;
            }
        }
        var Y = 0;
        var S;
        Y = Y^4294967295;
        for (var X = 0; X < U.length; X++) {
            var S = (Y^U.charCodeAt(X)) & 255;
            Y = (Y >>> 8)^I[S];
        }
        Y = Y^4294967295;
        var Z = "0123456789ABCDEF";
        return [Z.charAt((Y >>> 28) & 15), Z.charAt((Y >>> 24) & 15), Z.charAt((Y >>> 20) & 15), Z.charAt((Y >>> 16) & 15), 
        Z.charAt((Y >>> 12) & 15), Z.charAt((Y >>> 8) & 15), Z.charAt((Y >>> 4) & 15), Z.charAt((Y) & 15)].join("");
    }
    J.push(1706678977);
    function u()
    {
        if (!K) {
            return;
        }
        if (!N)
        {
            N = "";
            if (a.length > 0) {
                for (var U in a) {
                    if (N.indexOf(a[U].name) ==- 1) {
                        N += a[U].str;
                    }
                }
            }
            else {
                N = "unknown";
            }
            N += "||" + b;
        }
        var S = "";
        if (e) {
            S = "timezone: " + e + " execution time: " + (s - y);
        }
        else {
            S = "unknown";
        }
        var Y = [];
        Y.push('"version":"' + g + '"');
        Y.push('"start":' + y.getTime());
        Y.push('"elapsed":' + (s - y));
        Y.push('"userAgent":"' + o(navigator.userAgent) + '"');
        Y.push('"plugins":"' + o(N) + '"');
        if (O) {
            Y.push('"acceptCharset":"' + o(O) + '"');
        }
        if (i) {
            Y.push('"acceptLanguage":"' + o(i) + '"');
        }
        if (l) {
            Y.push('"flashVersion":"' + o(l) + '"');
        }
        if (e) {
            Y.push('"timeZone":' + e);
        }
        if (x) {
            Y.push('"lsUbid":"' + o(x) + '"');
        }
        if (G) {
            Y.push('"mercury":' + G);
        }
        if (v.length > 0) {
            Y.push('"errors":["' + v.join('","') + '"]');
        }
        var T = z("{" + Y.join(",") + "}");
        var X = c(T);
        var W = m(r(X + "#" + T));
        try
        {
            if (!f)
            {
                try {
                    f = document.createElement('<input name="metadata1">');
                }
                catch (V) {}
                if (!f || (f.nodeName != "INPUT")) {
                    f = document.createElement("input");
                    f.name = "metadata1";
                }
                f.type = "hidden";
                K.appendChild(f);
            }
            f.value = W;
        }
        catch (V) {
            C("rMD", V);
        }
    }
    function B()
    {
        var Z = 4022871197;
        function U(ag)
        {
            ag = ((typeof ag == "undefined") || (ag == null)) ? "" : ag.toString();
            for (var ae = 0; ae < ag.length; ae++)
            {
                Z += ag.charCodeAt(ae);
                var af = 0.02519603282416938 * Z;
                Z = af >>> 0;
                af -= Z;
                af *= Z;
                Z = af >>> 0;
                af -= Z;
                Z += af * 4294967296;
            }
            return (Z >>> 0) * 2.3283064365386963e - 10;
        }
        var ad = U(" ");
        var ac = U(" ");
        var aa = U(" ");
        var Y = 1;
        var ab = [document.body.innerHTML, navigator.userAgent, (new Date()).getTime()];
        for (var X in ab)
        {
            ad -= U(ab[X]);
            if (ad < 0) {
                ad += 1;
            }
            ac -= U(ab[X]);
            if (ac < 0) {
                ac += 1;
            }
            aa -= U(ab[X]);
            if (aa < 0) {
                aa += 1;
            }
        }
        function W()
        {
            var ae = 2091639 * ad + Y * 2.3283064365386963e - 10;
            ad = ac;
            ac = aa;
            aa = ae - (Y = ae | 0);
            return aa;
        }
        function V(ae)
        {
            return ("0000000000" + (W() * 4294967296).toString()).slice(-ae);
        }
        var T = "X" + V(2) + "-" + V(7) + "-" + V(7);
        var S = Math.floor((new Date()).getTime() / 1000);
        return T + ":" + S;
    }
    function q(S)
    {
        return (typeof (S) == "string") && S.match(/^\w{3}\-\d{7}\-\d{7}:\d+$/);
    }
    var F = "amznfbgid";
    function E()
    {
        try
        {
            if (typeof window.localStorage == "undefined") {
                return;
            }
            x = window.localStorage.getItem(F);
            if (!q(x)) {
                var S = B();
                window.localStorage.removeItem(F);
                window.localStorage.setItem(F, S);
                x = S;
            }
        }
        catch (T) {
            C("lLSU", T);
        }
    }
    function d(S)
    {
        try
        {
            if (typeof window.localStorage == "undefined") {
                return;
            }
            if (!q(S)) {
                return;
            }
            window.localStorage.removeItem(F);
            window.localStorage.setItem(F, S);
            x = S;
        }
        catch (T) {
            C("sLSU", T);
        }
    }
    var A = "/mercury9.swf";
    function P()
    {
        if (!A) {
            return null;
        }
        if (A.match(/^\w+:\/\//)) {
            return A;
        }
        if (A.charAt(0) == "/")
        {
            script = document.getElementById("fwcim-script");
            src = script && script.getAttribute("src");
            if (src) {
                return src.replace(/\/[^\/]+\.js$/, A);
            }
        }
        return "https://images-na.ssl-images-amazon.com/images/G/01/x-locale/common/login/mercury9.swf";
    }
    function h()
    {
        var S = document.domain;
        if (S.match(/development\.amazon\.com$/) || S.match(/desktop\.amazon\.com$/)) {
            return 0;
        }
        else
        {
            if (S.match(/\.com$/)) {
                return 1;
            }
            else
            {
                if (S.match(/\.co\.uk$/) || S.match(/\.de$/) || S.match(/\.fr$/) || S.match(/\.it$/)) {
                    return 2;
                }
                else {
                    if (S.match(/\.co\.jp$/)) {
                        return 3;
                    }
                    else {
                        if (S.match(/\.cn$/)) {
                            return 4;
                        }
                    }
                }
            }
        }
        return 1;
    }
    function Q()
    {
        try
        {
            if (!D) {
                throw new Error("No container");
            }
            if (!l || (l.split(".")[0] < 9)) {
                return;
            }
            var W = P();
            var U = x || B();
            var X = h();
            if (!W) {
                return;
            }
            var T = W + "?value1=" + U + "&vip=" + X;
            var S = document.createElement("div");
            S.id = "mercury";
            if (!n()) {
                S.setAttribute("style", "visibility:hidden");
            }
            S.innerHTML = '<param name="movie" value="' + T + '"/><param name="bgcolor" value="#ffffff" /><param name="AllowScriptAccess" value="always" /><embed src="' + T + '" bgcolor="#ffffff" AllowScriptAccess="always" width="0" height="0" />';
            D.appendChild(S);
        }
        catch (V) {
            C("eM", V);
            u();
        }
    }
    this.useMercury = function (S)
    {
        A = S;
    };
    this.prepareMercury = function () {};
    this.reportMercury = function (S, U)
    {
        try {
            d(S);
            G = U;
        }
        catch (T) {
            C("rM", T);
        }
        u();
    };
    J.push(3681020276);
    this.setAcceptCharset = function (S)
    {
        O = S;
    };
    this.setAcceptLanguage = function (S)
    {
        i = S;
    };
    this.profile = function (S)
    {
        try
        {
            y = new Date();
            if (!w(S)) {
                return;
            }
            D = document.getElementById("fwcim-container");
            if (navigator.plugins && (navigator.plugins.length > 0)) {
                p();
            }
            else {
                if (n() && R()) {
                    j();
                    H();
                }
            }
            L();
            M();
            E();
        }
        catch (T) {
            C("profile", T);
        }
        s = new Date();
        u();
        if (A) {
            setTimeout(Q, 1);
        }
    };
})();
document.writeln('<div id="fwcim-container"></div>');
function setMetadataF1(a)
{
    window.fwcim.reportMercury(a, '{"ubid":"' + a + '"}');
}
