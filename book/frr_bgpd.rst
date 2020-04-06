
FRR/BGPd Internals
===================

bgp instance structure
----------------------

.. code-block:: c++

   /* BGP instance structure.  */
   struct bgp {
           as_t as;
           char *name, *name_pretty;
           enum bgp_instance_type inst_type;
           vrf_id_t vrf_id;

           struct peer *peer_self; /* Self peer.  */
           struct list *peer;      /* BGP peer. */
           struct hash *peerhash;
           struct list *group;     /* BGP peer group.  */
           int dynamic_neighbors_limit; /* The maximum number of BGP dynamic neighbors that can be created */
           int dynamic_neighbors_count; /* The current number of BGP dynamic neighbors */
           struct hash *update_groups[BGP_AF_MAX];

           /*
            * Global statistics for update groups.
            */
           struct {
                   uint32_t join_events;
                   uint32_t prune_events;
                   uint32_t merge_events;
                   uint32_t split_events;
                   uint32_t updgrp_switch_events;
                   uint32_t peer_refreshes_combined;
                   uint32_t adj_count;
                   uint32_t merge_checks_triggered;

                   uint32_t updgrps_created;
                   uint32_t updgrps_deleted;
                   uint32_t subgrps_created;
                   uint32_t subgrps_deleted;
           } update_group_stats;

           uint16_t config; /* BGP configuration. BGP_CONFIG_XXX */
           struct in_addr router_id;        /* BGP router identifier */
           struct in_addr router_id_static; /* BGP router identifier */
           struct in_addr router_id_zebra;  /* BGP router identifier */
           struct in_addr cluster_id; /* BGP route reflector cluster ID.  */

           /* BGP confederation information.  */
           as_t confed_id;
           as_t *confed_peers;
           int confed_peers_cnt;

           struct thread *t_startup;          /* start-up timer on only once at the beginning */
           uint32_t v_maxmed_onstartup;       /* Duration of max-med on start-up */
           uint32_t maxmed_onstartup_value;   /* Max-med value when active on start-up */
           struct thread *t_maxmed_onstartup; /* non-null when max-med onstartup is on */
           uint8_t maxmed_onstartup_over;     /* Flag to make it effective only once */

           uint8_t v_maxmed_admin; /* 1/0 if max-med administrative is on/off */
           uint32_t maxmed_admin_value; /* Max-med value when administrative in on */
           uint8_t maxmed_active; /* 1/0 if max-med is active or not */
           uint32_t maxmed_value; /* Max-med value when its active */

           /* BGP update delay on startup */
           struct thread *t_update_delay;
           struct thread *t_establish_wait;
           uint8_t update_delay_over;
           uint8_t main_zebra_update_hold;
           uint8_t main_peers_update_hold;
           uint16_t v_update_delay;
           uint16_t v_establish_wait;
           char update_delay_begin_time[64];
           char update_delay_end_time[64];
           char update_delay_zebra_resume_time[64];
           char update_delay_peers_resume_time[64];
           uint32_t established;
           uint32_t restarted_peers;
           uint32_t implicit_eors;
           uint32_t explicit_eors;

           uint32_t flags;                                 /* BGP flags. BGP_FLAG_XXX */
           uint16_t af_flags[AFI_MAX][SAFI_MAX];           /* BGP Per AF flags */
           uint32_t af_peer_count[AFI_MAX][SAFI_MAX];      /* BGP per AF peer count */
           struct bgp_table *nexthop_cache_table[AFI_MAX]; /* Route table for next-hop lookup cache. */

           struct bgp_table *import_check_table[AFI_MAX]; /* Route table for import-check */
           struct bgp_table *connected_table[AFI_MAX];
           struct hash *address_hash;
           struct hash *tip_hash;

           struct bgp_table *route[AFI_MAX][SAFI_MAX]; /* Static route configuration.  */
           struct bgp_table *aggregate[AFI_MAX][SAFI_MAX]; /* Aggregate address configuration.  */
           struct bgp_table *rib[AFI_MAX][SAFI_MAX]; /* BGP routing information base.  */

           struct bgp_rmap table_map[AFI_MAX][SAFI_MAX]; /* BGP table route-map.  */
           struct list *redist[AFI_MAX][ZEBRA_ROUTE_MAX]; /* BGP redistribute configuration. */
           uint8_t allocate_mpls_labels[AFI_MAX][SAFI_MAX]; /* Allocate MPLS labels */

           /* Allocate hash entries to store policy routing information
            * The hash are used to host pbr rules somewhere. */
           struct hash *pbr_match_hash;
           struct hash *pbr_rule_hash;
           struct hash *pbr_action_hash;

           struct thread *t_rmap_def_originate_eval; /* timer to re-evaluate neighbor default-originate route-maps */

           uint8_t distance_ebgp[AFI_MAX][SAFI_MAX];
           uint8_t distance_ibgp[AFI_MAX][SAFI_MAX];
           uint8_t distance_local[AFI_MAX][SAFI_MAX];

           uint32_t default_local_pref; /* BGP default local-preference.  */
           uint32_t default_subgroup_pkt_queue_max; /* BGP default subgroup pkt queue max  */
           uint32_t default_holdtime;
           uint32_t default_keepalive;

           /* BGP graceful restart */
           uint32_t restart_time;
           uint32_t stalepath_time;

           /* Maximum-paths configuration */
           struct bgp_maxpaths_cfg {
                   uint16_t maxpaths_ebgp;
                   uint16_t maxpaths_ibgp;
                   uint16_t ibgp_flags; /* BGP_FLAG_IBGP_XXX */
           } maxpaths[AFI_MAX][SAFI_MAX];

           _Atomic uint32_t wpkt_quanta; // max # packets to write per i/o cycle
           _Atomic uint32_t rpkt_quanta; // max # packets to read per i/o cycle

           bool heuristic_coalesce; /* Automatic coalesce adjust on/off */
           uint32_t coalesce_time;  /* Actual coalesce time */
           bool autoshutdown;       /* Auto-shutdown new peers */
           struct bgp_addpath_bgp_data tx_addpath;

           /*
            * EVPN related information is skipped at my wiki ...
            */

           uint32_t vrf_flags;            /* vrf flags BGP_VRF_XXX */
           uint16_t vrf_rd_id;            /* unique ID for auto derivation of RD for this vrf */
           struct prefix_rd vrf_prd_auto; /* Automatically derived RD for this VRF */
           struct prefix_rd vrf_prd;      /* RD for this VRF */
           struct list *vrf_import_rtl; /* import rt list for the vrf instance */
           struct list *vrf_export_rtl; /* export rt list for the vrf instance */
           struct list *l2vnis; /* list of corresponding l2vnis (struct bgpevpn) */
           struct bgp_rmap adv_cmd_rmap[AFI_MAX][SAFI_MAX]; /* route map for advertise ipv4/ipv6 unicast (type-5 routes) */
           struct vpn_policy vpn_policy[AFI_MAX];
           struct bgp_pbr_config *bgp_pbr_cfg;
           struct hash *esihash; /* local esi hash table */
           uint32_t established_peers; /* Count of peers in established state */
   };

bgp peer structure

.. code-block:: c++

   struct peer { /* BGP neighbor structure. */

     pthread_mutex_t io_mtx;
     struct peer *doppelganger;
     unsigned char cur_event, last_event, last_major_event;
     uint16_t table_dump_index;

     /* afc is Address-Family-Configuration */
     uint8_t afc[AFI_MAX][SAFI_MAX];
     uint8_t afc_nego[AFI_MAX][SAFI_MAX];
     uint8_t afc_adv[AFI_MAX][SAFI_MAX];
     uint8_t afc_recv[AFI_MAX][SAFI_MAX];
     uint32_t cap;                       /* PEER_CAP_XXX */
     uint32_t af_cap[AFI_MAX][SAFI_MAX]; /* PEER_CAP_XXX */

     uint32_t flags_override, flags_invert, flags;
     char *tx_shutdown_message;
     uint8_t nsf[AFI_MAX][SAFI_MAX];
     uint32_t af_flags_override[AFI_MAX][SAFI_MAX];
     uint32_t af_flags_invert[AFI_MAX][SAFI_MAX];
     uint32_t af_flags[AFI_MAX][SAFI_MAX];
     enum bgp_addpath_strat addpath_type[AFI_MAX][SAFI_MAX];
     uint16_t sflags, af_sflags[AFI_MAX][SAFI_MAX]; /* Peer status flags. PEER_STATUS_XXX */

     uint32_t established, dropped;
     struct bgp_synchronize *sync[AFI_MAX][SAFI_MAX];
     unsigned long scount[AFI_MAX][SAFI_MAX]; /* Send prefix count. */
     struct bgp_filter filter[AFI_MAX][SAFI_MAX]; /* Filter structure. */
     uint8_t filter_override[AFI_MAX][SAFI_MAX][ (FILTER_MAX > RMAP_MAX) ? FILTER_MAX : RMAP_MAX ];
     struct prefix_list *orf_plist[AFI_MAX][SAFI_MAX]; /* ORF Prefix-list */
     unsigned long pcount[AFI_MAX][SAFI_MAX]; /* Prefix count. */

     /* Max prefix count. */
     unsigned long pmax[AFI_MAX][SAFI_MAX];
     uint8_t pmax_threshold[AFI_MAX][SAFI_MAX];
     uint16_t pmax_restart[AFI_MAX][SAFI_MAX];

     char allowas_in[AFI_MAX][SAFI_MAX]; /* allowas-in. */
     unsigned long weight[AFI_MAX][SAFI_MAX]; /* weight */

   };

.. code-block:: c++

   /* BGP MsgRcv */
   #define PEER_TOTAL_RX(peer) \
         atomic_load_explicit(&peer->open_in       , memory_order_relaxed) \
       + atomic_load_explicit(&peer->update_in     , memory_order_relaxed) \
       + atomic_load_explicit(&peer->notify_in     , memory_order_relaxed) \
       + atomic_load_explicit(&peer->refresh_in    , memory_order_relaxed) \
       + atomic_load_explicit(&peer->keepalive_in  , memory_order_relaxed) \
       + atomic_load_explicit(&peer->dynamic_cap_in, memory_order_relaxed)

   /* BGP MsgSnt */
   #define PEER_TOTAL_TX(peer) \
         atomic_load_explicit(&peer->open_out       , memory_order_relaxed) \
       + atomic_load_explicit(&peer->update_out     , memory_order_relaxed) \
       + atomic_load_explicit(&peer->notify_out     , memory_order_relaxed) \
       + atomic_load_explicit(&peer->refresh_out    , memory_order_relaxed) \
       + atomic_load_explicit(&peer->keepalive_out  , memory_order_relaxed) \
       + atomic_load_explicit(&peer->dynamic_cap_out, memory_order_relaxed)

bgp path attribute structure
-----------------------------

.. code-block:: c++

   /* BGP core attribute structure. */
   struct attr {
     struct aspath *aspath;       /* AS Path structure */
     struct community *community; /* Community structure */
     unsigned long refcnt;        /* Reference count of this attribute. */
     uint64_t flag;               /* Flag of attribute is set or not. */

     struct in_addr nexthop; /* Apart from in6_addr, the remaining static attributes */
     uint32_t med;
     uint32_t local_pref;
     ifindex_t nh_ifindex;

     uint8_t origin;              /* Path origin attribute */
     enum pta_type pmsi_tnl_type; /* PMSI tunnel type (RFC 6514). */
     uint32_t rmap_change_flags;

     struct in6_addr mp_nexthop_global; /* Multi-Protocol Nexthop, AFI IPv6 (global) */
     struct in6_addr mp_nexthop_local;  /* Multi-Protocol Nexthop, AFI IPv6 (local) */
     ifindex_t nh_lla_ifindex;          /* ifIndex corresponding to mp_nexthop_local. */

     struct ecommunity *ecommunity; /* Extended Communities attribute. */
     struct lcommunity *lcommunity; /* Large Communities attribute. */
     struct cluster_list *cluster;  /* Route-Reflector Cluster attribute */

     struct transit *transit; /* Unknown transitive attribute. */
     struct in_addr mp_nexthop_global_in;
     struct in_addr aggregator_addr; /* Aggregator Router ID attribute */
     struct in_addr originator_id;   /* Route Reflector Originator attribute */

     uint32_t weight;    /* Local weight, not actually an attribute */
     as_t aggregator_as; /* Aggregator ASN */

     uint8_t mp_nexthop_len;           /* MP Nexthop length */
     uint8_t mp_nexthop_prefer_global; /* MP Nexthop preference */

     uint8_t sticky;       /* Static MAC for EVPN */
     uint8_t default_gw;   /* Flag for default gateway extended community in EVPN */
     uint8_t router_flag;  /* NA router flag (R-bit) support in EVPN */
     route_tag_t tag;      /* route tag */
     uint32_t label_index; /* Label index */
     mpls_label_t label;   /* MPLS label */

     uint16_t encap_tunneltype;         /* grr */
     struct bgp_attr_encap_subtlv *encap_subtlvs; /* rfc5512 */
     struct bgp_route_evpn evpn_overlay; /* EVPN */
     uint32_t mm_seqnum; /* EVPN MAC Mobility sequence number, if any. */
     struct ethaddr rmac; /* EVPN local router-mac */
     uint8_t distance; /* Distance as applied by Route map */
     uint32_t rmap_table_id; /* rmap set table */
   };

bgp vpn_policy structure
-----------------------------

.. code-block:: c++

   struct vpn_policy {
     struct bgp *bgp; /* parent */
     afi_t afi;
     struct ecommunity *rtlist[BGP_VPN_POLICY_DIR_MAX];
     struct ecommunity *import_redirect_rtlist;
     char *rmap_name[BGP_VPN_POLICY_DIR_MAX];
     struct route_map *rmap[BGP_VPN_POLICY_DIR_MAX];

     /* should be mpls_label_t? */
     uint32_t tovpn_label; /* may be MPLS_LABEL_NONE */
     uint32_t tovpn_zebra_vrf_label_last_sent;
     struct prefix_rd tovpn_rd;
     struct prefix tovpn_nexthop; /* unset => set to 0 */
     uint32_t flags;
   #define BGP_VPN_POLICY_TOVPN_LABEL_AUTO        (1 << 0)
   #define BGP_VPN_POLICY_TOVPN_RD_SET            (1 << 1)
   #define BGP_VPN_POLICY_TOVPN_NEXTHOP_SET       (1 << 2)

     /*
      * If we are importing another vrf into us keep a list of
      * vrf names that are being imported into us.
      */
     struct list *import_vrf;

     /*
      * if we are being exported to another vrf keep a list of
      * vrf names that we are being exported to.
      */
     struct list *export_vrf;
   };

bgp node information
--------------------

.. code-block:: c++

   struct bgp_node {
     /*
      * CAUTION
      *
      * These fields must be the very first fields in this structure.
      *
      * @see bgp_node_to_rnode
      * @see bgp_node_from_rnode
      */
     ROUTE_NODE_FIELDS

     struct bgp_adj_out_rb adj_out;
     struct bgp_adj_in *adj_in;
     struct bgp_node *prn;
     STAILQ_ENTRY(bgp_node) pq;
     uint64_t version;

     mpls_label_t local_label;

     uint8_t flags;
   #define BGP_NODE_PROCESS_SCHEDULED  (1 << 0)
   #define BGP_NODE_USER_CLEAR             (1 << 1)
   #define BGP_NODE_LABEL_CHANGED          (1 << 2)
   #define BGP_NODE_REGISTERED_FOR_LABEL   (1 << 3)

     struct bgp_addpath_node_data tx_addpath;

     enum bgp_path_selection_reason reason;
   };

struct bgp_node
---------------

.. code-block:: c++

   struct bgp_node {
     /*
      * CAUTION
      *
      * These fields must be the very first fields in this structure.
      *
      * @see bgp_node_to_rnode
      * @see bgp_node_from_rnode
      */
     ROUTE_NODE_FIELDS

     struct bgp_adj_out_rb adj_out;

     struct bgp_adj_in *adj_in;

     struct bgp_node *prn;

     STAILQ_ENTRY(bgp_node) pq;

     uint64_t version;

     mpls_label_t local_label;

     uint8_t flags;
   #define BGP_NODE_PROCESS_SCHEDULED  (1 << 0)
   #define BGP_NODE_USER_CLEAR             (1 << 1)
   #define BGP_NODE_LABEL_CHANGED          (1 << 2)
   #define BGP_NODE_REGISTERED_FOR_LABEL   (1 << 3)

     struct bgp_addpath_node_data tx_addpath;

      enum bgp_path_selection_reason reason;
    };

struct bgp_path_info
---------------------

.. code-block:: c++

   struct bgp_path_info {
           /* For linked list. */
           struct bgp_path_info *next;
           struct bgp_path_info *prev;

           /* For nexthop linked list */
           LIST_ENTRY(bgp_path_info) nh_thread;

           /* Back pointer to the prefix node */
           struct bgp_node *net;

           /* Back pointer to the nexthop structure */
           struct bgp_nexthop_cache *nexthop;

           /* Peer structure.  */
           struct peer *peer;

           /* Attribute structure.  */
           struct attr *attr;

           /* Extra information */
           struct bgp_path_info_extra *extra;


           /* Multipath information */
           struct bgp_path_info_mpath *mpath;

           /* Uptime.  */
           time_t uptime;

           /* reference count */
           int lock;

           /* BGP information status.  */
           uint16_t flags;
   #define BGP_PATH_IGP_CHANGED (1 << 0)
   #define BGP_PATH_DAMPED (1 << 1)
   #define BGP_PATH_HISTORY (1 << 2)
   #define BGP_PATH_SELECTED (1 << 3)
   #define BGP_PATH_VALID (1 << 4)
   #define BGP_PATH_ATTR_CHANGED (1 << 5)
   #define BGP_PATH_DMED_CHECK (1 << 6)
   #define BGP_PATH_DMED_SELECTED (1 << 7)
   #define BGP_PATH_STALE (1 << 8)
   #define BGP_PATH_REMOVED (1 << 9)
   #define BGP_PATH_COUNTED (1 << 10)
   #define BGP_PATH_MULTIPATH (1 << 11)
   #define BGP_PATH_MULTIPATH_CHG (1 << 12)
   #define BGP_PATH_RIB_ATTR_CHG (1 << 13)
   #define BGP_PATH_ANNC_NH_SELF (1 << 14)

           /* BGP route type.  This can be static, RIP, OSPF, BGP etc.  */
           uint8_t type;

           /* When above type is BGP.  This sub type specify BGP sub type
              information.  */
           uint8_t sub_type;
   #define BGP_ROUTE_NORMAL       0
   #define BGP_ROUTE_STATIC       1
   #define BGP_ROUTE_AGGREGATE    2
   #define BGP_ROUTE_REDISTRIBUTE 3
   #ifdef ENABLE_BGP_VNC
   # define BGP_ROUTE_RFP          4
   #endif
   #define BGP_ROUTE_IMPORTED     5        /* from another bgp instance/safi */

           unsigned short instance;

           /* Addpath identifiers */
           uint32_t addpath_rx_id;
           struct bgp_addpath_info_data tx_addpath;
   };

