
FRR/ZEBRA Internals
====================

ZAPI server-side (forcusing `ZEBRA_ROUTE_ADD`)
-----------------------------------------------

.. code-block:: shell

   $ cat lib/zclient.h | grep "Zebra message types" -A 15
   /* Zebra message types. */
   typedef enum {
           ZEBRA_INTERFACE_ADD,
           ZEBRA_INTERFACE_DELETE,
           ZEBRA_INTERFACE_ADDRESS_ADD,
           ZEBRA_INTERFACE_ADDRESS_DELETE,
           ZEBRA_INTERFACE_UP,
           ZEBRA_INTERFACE_DOWN,
           ZEBRA_INTERFACE_SET_MASTER,
           ZEBRA_INTERFACE_SET_PROTODOWN,
           ZEBRA_ROUTE_ADD,
           ZEBRA_ROUTE_DELETE,
           ZEBRA_ROUTE_NOTIFY_OWNER,
           ZEBRA_REDISTRIBUTE_ADD,
           ZEBRA_REDISTRIBUTE_DELETE,
           ZEBRA_REDISTRIBUTE_DEFAULT_ADD,

   $ cat zebra/zapi_msg.c | grep "void (\*zserv_handlers" -A 10
   void (*zserv_handlers[])(ZAPI_HANDLER_ARGS) = {
           [ZEBRA_ROUTER_ID_ADD] = zread_router_id_add,
           [ZEBRA_ROUTER_ID_DELETE] = zread_router_id_delete,
           [ZEBRA_INTERFACE_ADD] = zread_interface_add,
           [ZEBRA_INTERFACE_DELETE] = zread_interface_delete,
           [ZEBRA_INTERFACE_SET_PROTODOWN] = zread_interface_set_protodown,
           [ZEBRA_ROUTE_ADD] = zread_route_add,
           [ZEBRA_ROUTE_DELETE] = zread_route_del,
           [ZEBRA_REDISTRIBUTE_ADD] = zebra_redistribute_add,
           [ZEBRA_REDISTRIBUTE_DELETE] = zebra_redistribute_delete,
           [ZEBRA_REDISTRIBUTE_DEFAULT_ADD] = zebra_redistribute_default_add,

   $ cat zebra/zapi_msg.c | grep "static void zread_route_add" -A 10
   static void zread_route_add(ZAPI_HANDLER_ARGS)
   {
           struct stream *s;
           struct zapi_route api;
           struct zapi_nexthop *api_nh;
           afi_t afi;
           struct prefix_ipv6 *src_p = NULL;
           struct route_entry *re;
           struct nexthop *nexthop = NULL;
           int i, ret;
           vrf_id_t vrf_id = 0;
           ...
   }

   $ cat zebra/zserv.h | grep ZAPI_HANDLER_ARGS -A2
   #define ZAPI_HANDLER_ARGS \
           struct zserv *client, struct zmsghdr *hdr, \
           struct stream *msg, struct zebra_vrf *zvrf

   $ cat lib/zclient.h | grep "struct zmsghdr {" -A7
   struct zmsghdr {
           uint16_t length;
           /* Always set to 255 in new zserv */
           uint8_t marker;
           uint8_t version;
           vrf_id_t vrf_id;
           uint16_t command;
   };

ZAPI client-side (forcusing `ZEBRA_ROUTE_ADD`)
-----------------------------------------------

.. code-block:: shell

   $ cat static_zebra.c | grep "extern void static_zebra_route_add(" -A10000 | less
   extern void static_zebra_route_add(struct route_node *rn,
                                      struct static_route *si_changed,
                                      vrf_id_t vrf_id, safi_t safi, bool install)
   {
           struct static_route *si = rn->info;
           const struct prefix *p, *src_pp;

           struct static_route *si = rn->info;
           const struct prefix *p, *src_pp;
           struct zapi_nexthop *api_nh;
           struct zapi_route api;
           uint32_t nh_num = 0;
   ...(snip)...
           zclient_route_send(install ?
                              ZEBRA_ROUTE_ADD : ZEBRA_ROUTE_DELETE,
                              zclient, &api);
   }

   $ cat lib/zclient.c  | grep zclient_route_send -A6
   int zclient_route_send(uint8_t cmd, struct zclient *zclient,
                          struct zapi_route *api)
   {
           if (zapi_route_encode(cmd, zclient->obuf, api) < 0)
                   return -1;
           return zclient_send_message(zclient);
   }

VTYSH
--------

Building
---------

.. code-block:: shell

   ./configure \
     --prefix=/usr --includedir=\${prefix}/include \
     --enable-exampledir=\${prefix}/share/doc/frr/examples \
     --bindir=\${prefix}/bin --sbindir=\${prefix}/lib/frr \
     --libdir=\${prefix}/lib/frr --libexecdir=\${prefix}/lib/frr \
     --localstatedir=/var/run/frr --sysconfdir=/etc/frr \
     --with-moduledir=\${prefix}/lib/frr/modules \
     --with-libyang-pluginsdir=\${prefix}/lib/frr/libyang_plugins \
     --enable-configfile-mask=0640 --enable-logfile-mask=0640 \
     --enable-snmp=agentx --enable-multipath=64 --enable-user=frr \
     --enable-group=frr --enable-vty-group=frrvty --with-pkg-git-version \
     --disable-ripd --disable-ripngd --disable-ospfd --disable-ospf6d \
     --disable-ldpd --disable-nhrpd --disable-eigrpd --disable-babeld \
     --disable-isisd --disable-pimd --disable-pbrd --disable-fabricd \
     --disable-vrrpd

daemons
--------

.. code-block:: text

   bgpd=no
   ospfd=no
   ospf6d=no
   ripd=no
   ripngd=no
   isisd=no
   pimd=no
   ldpd=no
   nhrpd=no
   eigrpd=no
   babeld=no
   sharpd=no
   pbrd=no
   bfdd=no
   fabricd=no
   vrrpd=no
   vtysh_enable=yes
   zebra_options="  -A 127.0.0.1 -s 90000000"
   bgpd_options="   -A 127.0.0.1"
   ospfd_options="  -A 127.0.0.1"
   ospf6d_options=" -A ::1"
   ripd_options="   -A 127.0.0.1"
   ripngd_options=" -A ::1"
   isisd_options="  -A 127.0.0.1"
   pimd_options="   -A 127.0.0.1"
   ldpd_options="   -A 127.0.0.1"
   nhrpd_options="  -A 127.0.0.1"
   eigrpd_options=" -A 127.0.0.1"
   babeld_options=" -A 127.0.0.1"
   sharpd_options=" -A 127.0.0.1"
   pbrd_options="   -A 127.0.0.1"
   staticd_options="-A 127.0.0.1"
   bfdd_options="   -A 127.0.0.1"
   fabricd_options="-A 127.0.0.1"
   vrrpd_options="  -A 127.0.0.1"

