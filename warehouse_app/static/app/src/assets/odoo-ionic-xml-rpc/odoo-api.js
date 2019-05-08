function OdooApi (host, db) {
    
if (!host.match('\/$')) {
    host = host + '/';
}
        
this.odoo_host = host;
this.odoo_db = db;
this.odoo_uid = false;
this.odoo_user = false;
this.odoo_password = false;
this.context = {'lang': 'es_ES'}, //odoo_api,
    
this.login = function(user, password) {
    this.odoo_user = user;
    this.odoo_password = password;
        
    var odoo_api = this;
    odoo_api.context = {'lang': 'es_ES'}
    var promise = new Promise(function(resolve, reject) {
        $.xmlrpc({
            headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
            url: odoo_api.odoo_host + 'xmlrpc/common',
            methodName: 'login',
            params: [odoo_api.odoo_db, user, password],
            timeout: 10000,
            context:odoo_api.context,
            success: function(response, status, jqXHR) {
                if (response[0]) {
                    odoo_api.odoo_uid = response[0];
                    resolve(response[0]);
                } else {
                    odoo_api.odoo_uid = false;
                    reject()
                }
            },
            error: function(jqXHR, status, error) {
                odoo_api.uid = false;
                reject()
            }
        });    
    });

    return promise
};
    
this.search = function(model, domain) {
        
    var odoo_api = this;
    var ctx ={'lang': 'es_ES'}
    if (!domain)
        domain = [];
        
    var promise = new Promise(function(resolve, reject) {
        $.xmlrpc({
            headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
            url: odoo_api.odoo_host + 'xmlrpc/object',
            methodName: 'execute',
            params: [odoo_api.odoo_db, odoo_api.odoo_uid, odoo_api.odoo_password,
                     model, 'search', domain],
            timeout: 10000,
            context:odoo_api.context,
            success: function(response, status, jqXHR) {
                if (response[0]) {
                    resolve(response[0]);
                } else {
                    reject()
                }
            },
            error: function(jqXHR, status, error) {
                reject()
            }
        });    
    });

    return promise
};


this.search_read = function(model, domain, fields, offset, limit) {
   
    var odoo_api = this;
    var order = false
    if (!domain)
        domain = [];
    var promise = new Promise(function(resolve, reject) {
        $.xmlrpc({
            headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
            url: odoo_api.odoo_host + 'xmlrpc/object',
            methodName: 'execute',
            params: [odoo_api.odoo_db, odoo_api.odoo_uid, odoo_api.odoo_password,
                    model, 'search_read', domain, fields, offset, limit, order, odoo_api.context],
            timeout: 10000,
            context:odoo_api.context,
            success: function(response, status, jqXHR) {
                if (response[0]) {
                    resolve(response[0]);
                } else {
                    reject()
                }
            },
            error: function(jqXHR, status, error) {
                reject()
            }
        });    
    });

return promise
};

this.read = function(model, ids, fields) {
        
    var odoo_api = this;
    
    var promise = new Promise(function(resolve, reject) {
        $.xmlrpc({
            headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
            url: odoo_api.odoo_host + 'xmlrpc/object',
            methodName: 'execute',
            params: [odoo_api.odoo_db, odoo_api.odoo_uid, odoo_api.odoo_password,
                     model, 'read', ids, fields, odoo_api.context],
            timeout: 10000,
            context:odoo_api.context,
            success: function(response, status, jqXHR) {
                if (response[0]) {
                    resolve(response[0]);
                } else {
                    reject()
                }
            },
            error: function(jqXHR, status, error) {
                reject()
            }
        });    
    });

    return promise
};

this.write = function(model, id, data) {
        
    var odoo_api = this;
    var ctx ={'lang': 'es_ES'} 
    var promise = new Promise(function(resolve, reject) {
        $.xmlrpc({
            headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
            url: odoo_api.odoo_host + 'xmlrpc/object',
            methodName: 'execute',
            params: [odoo_api.odoo_db, odoo_api.odoo_uid, odoo_api.odoo_password,
                     model, 'write', id, data, odoo_api.context],
            timeout: 10000,
            context:odoo_api.context,
            success: function(response, status, jqXHR) {
                if (response[0]) {
                    resolve(response[0]);
                } else {
                    reject()
                }
            },
            error: function(jqXHR, status, error) {
                reject()
            }
        });    
    });

    return promise
};

this.create = function(model, data) {
    
    var odoo_api = this;
    
    var promise = new Promise(function(resolve, reject) {
        $.xmlrpc({
            headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
            url: odoo_api.odoo_host + 'xmlrpc/object',
            methodName: 'execute',
            params: [odoo_api.odoo_db, odoo_api.odoo_uid, odoo_api.odoo_password,
                     model, 'create', data, odoo_api.context],
            timeout: 10000,
            context: odoo_api.context,
            success: function(response, status, jqXHR) {
                if (response[0]) {
                    resolve(response[0]);
                } else {
                    reject()
                }
            },
            error: function(jqXHR, status, error) {
                reject()
            }
        });    
    });

    return promise
};

this.delete = function(model, ids) {
        
    var odoo_api = this;
        
    var promise = new Promise(function(resolve, reject) {
        $.xmlrpc({
            headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
            url: odoo_api.odoo_host + 'xmlrpc/object',
            methodName: 'execute',
            params: [odoo_api.odoo_db, odoo_api.odoo_uid, odoo_api.odoo_password,
                     model, 'unlink', ids],
            timeout: 10000,
            context: odoo_api.context,
            success: function(response, status, jqXHR) {
                if (response[0]) {
                    resolve(response[0]);
                } else {
                    reject()
                }
            },
            error: function(jqXHR, status, error) {
                reject()
            }
        });    
    });

    return promise
};
this.call = function(model, method, values) {
    
    var odoo_api = this;
    var promise = new Promise(function(resolve, reject) {
        $.xmlrpc({
            headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
            url: odoo_api.odoo_host + 'xmlrpc/object',
            methodName: 'execute',
            params: [odoo_api.odoo_db, odoo_api.odoo_uid, odoo_api.odoo_password,
                    model, method, values, odoo_api.context],
            timeout: 10000,
            context: odoo_api.context,
            success: function(response, status, jqXHR) {
                if (response[0]) {
                    resolve(response[0]);
                } else {
                    reject()
                }
            },
            error: function(jqXHR, status, error) {
                reject()
            }
        });    
});

return promise
};
this.call2 = function(model, method, args) {
        
    var odoo_api = this;
    var params = [odoo_api.odoo_db, odoo_api.odoo_uid, odoo_api.odoo_password, model, method, args]
    
    //for(var arg = 0; arg < arguments.length; ++ arg) {
    //    params.push(arguments[arg])
    //}
    console.log(params)
    var promise = new Promise(function(resolve, reject) {
        $.xmlrpc({
            headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
            url: odoo_api.odoo_host + 'xmlrpc/object',
            methodName: 'execute',
            params: params,
            timeout: 10000,
            context: odoo_api,
            success: function(response, status, jqXHR) {
                if (response[0]) {
                    resolve(response[0]);
                } else {
                    reject()
                }
            },
            error: function(jqXHR, status, error) {
                reject()
            }
        });    
    });

    return promise
};
}