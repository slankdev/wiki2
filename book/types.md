
# Structure Types and Enums Cheatsheet

## netlink
```
/* linux/netlink.h */

struct nlmsghdr {
  u32 nlmsg_len;
  u16 nlmsg_type;
  u16 nlmsg_flags;
  u32 nlmsg_seq;
  u32 nlmsg_pid;
};

#define NLM_F_REQUEST         0x001  /* It is request message.   */
#define NLM_F_MULTI           0x002  /* Multipart message, terminated by NLMSG_DONE */
#define NLM_F_ACK             0x004  /* Reply with ack, with zero or error code */
#define NLM_F_ECHO            0x008  /* Echo this request    */
#define NLM_F_DUMP_INTR       0x010  /* Dump was inconsistent due to sequence change */
#define NLM_F_DUMP_FILTERED   0x020  /* Dump was filtered as requested */
#define NLM_F_ROOT            0x100 /* specify tree root  */
#define NLM_F_MATCH           0x200 /* return all matching  */
#define NLM_F_ATOMIC          0x400 /* atomic GET   */
#define NLM_F_DUMP            (NLM_F_ROOT|NLM_F_MATCH)
#define NLM_F_REPLACE         0x100 /* Override existing    */
#define NLM_F_EXCL            0x200 /* Do not touch, if it exists */
#define NLM_F_CREATE          0x400 /* Create, if it does not exist */
#define NLM_F_APPEND          0x800 /* Add to end of list   */
#define NLM_F_NONREC          0x100 /* Do not delete recursively  */
#define NLM_F_CAPPED          0x100 /* request was capped */
#define NLM_F_ACK_TLVS        0x200 /* extended ACK TVLs were included */

enum {
        RTM_BASE           =  16,
        RTM_NEWLINK        =  16, RTM_DELLINK        , RTM_GETLINK, RTM_SETLINK,
        RTM_NEWADDR        =  20, RTM_DELADDR        , RTM_GETADDR,
        RTM_NEWROUTE       =  24, RTM_DELROUTE       , RTM_GETROUTE,
        RTM_NEWNEIGH       =  28, RTM_DELNEIGH       , RTM_GETNEIGH,
        RTM_NEWRULE        =  32, RTM_DELRULE        , RTM_GETRULE,
        RTM_NEWQDISC       =  36, RTM_DELQDISC       , RTM_GETQDISC,
        RTM_NEWTCLASS      =  40, RTM_DELTCLASS      , RTM_GETTCLASS,
        RTM_NEWTFILTER     =  44, RTM_DELTFILTER     , RTM_GETTFILTER,
        RTM_NEWACTION      =  48, RTM_DELACTION      , RTM_GETACTION,
        RTM_NEWPREFIX      =  52, RTM_GETMULTICAST= 58, RTM_GETANYCAST= 62,
        RTM_NEWNEIGHTBL    =  64, RTM_GETNEIGHTBL= 66, RTM_SETNEIGHTBL,
        RTM_NEWNDUSEROPT   =  68,
        RTM_NEWADDRLABEL   =  72, RTM_DELADDRLABEL   , RTM_GETADDRLABEL,
        RTM_GETDCB         =  78, RTM_SETDCB         ,
        RTM_NEWNETCONF     =  80, RTM_DELNETCONF     , RTM_GETNETCONF= 82,
        RTM_NEWMDB         =  84, RTM_DELMDB         , RTM_GETMDB,
        RTM_NEWNSID        =  88, RTM_DELNSID        , RTM_GETNSID,
        RTM_NEWSTATS       =  92, RTM_GETSTATS = 94,
        RTM_NEWCACHEREPORT =  96,
        RTM_NEWCHAIN       = 100, RTM_DELCHAIN       , RTM_GETCHAIN,
        RTM_NEWNEXTHOP     = 104, RTM_DELNEXTHOP     , RTM_GETNEXTHOP,
        __RTM_MAX,
#define RTM_MAX         (((__RTM_MAX + 3) & ~3) - 1)
}
```

```
struct iovec {
  void  *iov_base;
  size_t iov_len;
};
```

## rtnl

```
/* linux/rtnetlink.h */

struct rtattr {
  u16 rta_len;
  u16 rta_type;
};

struct rtmsg {
  u8 rtm_family;
  u8 rtm_dst_len;
  u8 rtm_src_len;
  u8 rtm_tos;
  u8 rtm_table;  /* Routing table id */
  u8 rtm_protocol; /* Routing protocol; see below  */
  u8 rtm_scope;  /* See below */
  u8 rtm_type; /* See below  */
  u32 rtm_flags;
};
```

```
/* linux/nexthop.h */

struct nhmsg {
  u8 nh_family;
  u8 nh_scope;     /* return only */
  u8 nh_protocol;  /* Routing protocol that installed nh */
  u8 resvd;
  u32 nh_flags;     /* RTNH_F flags */
};

struct nexthop_grp {
  u32 id;   /* nexthop id - must exist */
  u8  weight;   /* weight of this nexthop */
  u8  resvd1;
  u16 resvd2;
};

enum {
  NEXTHOP_GRP_TYPE_MPATH,  /* default type if not specified */
  __NEXTHOP_GRP_TYPE_MAX,
#define NEXTHOP_GRP_TYPE_MAX (__NEXTHOP_GRP_TYPE_MAX - 1)
};

enum {
  NHA_UNSPEC,
  NHA_ID,         /* u32; id for nexthop. id == 0 means auto-assign */
  NHA_GROUP,      /* array of nexthop_grp */
  NHA_GROUP_TYPE, /* u16 one of NEXTHOP_GRP_TYPE */
                  /* if NHA_GROUP attribute is added, no other attributes can be set */
  NHA_BLACKHOLE,  /* flag; nexthop used to blackhole packets */
                  /* if NHA_BLACKHOLE is added, OIF, GATEWAY, ENCAP can not be set */
  NHA_OIF,        /* u32; nexthop device */
  NHA_GATEWAY,    /* be32 (IPv4) or in6_addr (IPv6) gw address */
  NHA_ENCAP_TYPE, /* u16; lwt encap type */
  NHA_ENCAP,      /* lwt encap data */

  /* NHA_OIF can be appended to dump request to return only
   * nexthops using given device
   */
  NHA_GROUPS,     /* flag; only return nexthop groups in dump */
  NHA_MASTER,     /* u32;  only return nexthops with given master dev */
  __NHA_MAX,
};
```

## genl
```
struct genlmsghdr {
  u8 cmd;
  u8 version;
  u16 reserved;
};
```

```
cmd := {
  /* CTRL_CMD_XXX on /usr/include/genetlink.h */
  CTRL_CMD_GETFAMILY,
  etc,...

  /* SEG6_CMD_XXX on /usr/include/linux/seg6_genl.h */
  SEG6_CMD_SET_TUNSRC,
  SEG6_CMD_GET_TUNSRC,
  etc,..
}

version := { 0,1,2,...? }
reserved := uint16_t(0)
```

## struct msghdr
```
struct msghdr {
  void         *msg_name;
  socklen_t     msg_namelen;
  struct iovec *msg_iov;
  size_t        msg_iovlen;
  void         *msg_control;
  size_t        msg_controllen;
  int           msg_flags;
};
```

## About seg6 / seg6local
```
/* /usr/include/linux/seg6.h */
struct ipv6_sr_hdr {
  __u8  nexthdr;
  __u8  hdrlen;
  __u8  type;
  __u8  segments_left;
  __u8  first_segment; /* Represents the last_entry field of SRH */
  __u8  flags;
  __u16 tag;

  struct in6_addr segments[0];
};
```

```
/* usr/include/linux/seg6_iptunnel.h */
enum {
  SEG6_IPTUNNEL_UNSPEC,
  SEG6_IPTUNNEL_SRH,
  __SEG6_IPTUNNEL_MAX,
};
enum {
  SEG6_IPTUN_MODE_INLINE,
  SEG6_IPTUN_MODE_ENCAP,
  SEG6_IPTUN_MODE_L2ENCAP,
};

struct seg6_iptunnel_encap {
  int mode;
  struct ipv6_sr_hdr srh[0];
};
```

```
/* linux/lwtunnel.h */
enum lwtunnel_encap_types {
  LWTUNNEL_ENCAP_NONE,
  LWTUNNEL_ENCAP_MPLS,
  LWTUNNEL_ENCAP_IP,
  LWTUNNEL_ENCAP_ILA,
  LWTUNNEL_ENCAP_IP6,
  LWTUNNEL_ENCAP_SEG6,
  LWTUNNEL_ENCAP_BPF,
  LWTUNNEL_ENCAP_SEG6_LOCAL,
  __LWTUNNEL_ENCAP_MAX,
};
```

```
/* linux/seg6_local.h */

enum {
  SEG6_LOCAL_UNSPEC,
  SEG6_LOCAL_ACTION,
  SEG6_LOCAL_SRH,
  SEG6_LOCAL_TABLE,
  SEG6_LOCAL_NH4,
  SEG6_LOCAL_NH6,
  SEG6_LOCAL_IIF,
  SEG6_LOCAL_OIF,
  __SEG6_LOCAL_MAX,
};

enum {
  SEG6_LOCAL_ACTION_UNSPEC  = 0,
  SEG6_LOCAL_ACTION_END     = 1,
  SEG6_LOCAL_ACTION_END_X   = 2,
  SEG6_LOCAL_ACTION_END_T   = 3,
  SEG6_LOCAL_ACTION_END_DX2 = 4,
  SEG6_LOCAL_ACTION_END_DX6 = 5,
  SEG6_LOCAL_ACTION_END_DX4 = 6,
  SEG6_LOCAL_ACTION_END_DT6 = 7,
  SEG6_LOCAL_ACTION_END_DT4 = 8,
  SEG6_LOCAL_ACTION_END_B6  = 9,
  SEG6_LOCAL_ACTION_END_B6_ENCAP  = 10,
  SEG6_LOCAL_ACTION_END_BM  = 11,
  SEG6_LOCAL_ACTION_END_S   = 12,
  SEG6_LOCAL_ACTION_END_AS  = 13,
  SEG6_LOCAL_ACTION_END_AM  = 14,
  __SEG6_LOCAL_ACTION_MAX,
};
```

