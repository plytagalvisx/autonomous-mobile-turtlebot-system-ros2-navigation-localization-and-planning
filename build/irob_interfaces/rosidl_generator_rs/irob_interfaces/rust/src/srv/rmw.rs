#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



#[link(name = "irob_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__irob_interfaces__srv__GetGoal_Request() -> *const std::ffi::c_void;
}

#[link(name = "irob_interfaces__rosidl_generator_c")]
extern "C" {
    fn irob_interfaces__srv__GetGoal_Request__init(msg: *mut GetGoal_Request) -> bool;
    fn irob_interfaces__srv__GetGoal_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetGoal_Request>, size: usize) -> bool;
    fn irob_interfaces__srv__GetGoal_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetGoal_Request>);
    fn irob_interfaces__srv__GetGoal_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetGoal_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GetGoal_Request>) -> bool;
}

// Corresponds to irob_interfaces__srv__GetGoal_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetGoal_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !irob_interfaces__srv__GetGoal_Request__init(&mut msg as *mut _) {
        panic!("Call to irob_interfaces__srv__GetGoal_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetGoal_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { irob_interfaces__srv__GetGoal_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { irob_interfaces__srv__GetGoal_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { irob_interfaces__srv__GetGoal_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetGoal_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetGoal_Request where Self: Sized {
  const TYPE_NAME: &'static str = "irob_interfaces/srv/GetGoal_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__irob_interfaces__srv__GetGoal_Request() }
  }
}


#[link(name = "irob_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__irob_interfaces__srv__GetGoal_Response() -> *const std::ffi::c_void;
}

#[link(name = "irob_interfaces__rosidl_generator_c")]
extern "C" {
    fn irob_interfaces__srv__GetGoal_Response__init(msg: *mut GetGoal_Response) -> bool;
    fn irob_interfaces__srv__GetGoal_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetGoal_Response>, size: usize) -> bool;
    fn irob_interfaces__srv__GetGoal_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetGoal_Response>);
    fn irob_interfaces__srv__GetGoal_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetGoal_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GetGoal_Response>) -> bool;
}

// Corresponds to irob_interfaces__srv__GetGoal_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_x: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_y: f64,

}



impl Default for GetGoal_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !irob_interfaces__srv__GetGoal_Response__init(&mut msg as *mut _) {
        panic!("Call to irob_interfaces__srv__GetGoal_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetGoal_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { irob_interfaces__srv__GetGoal_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { irob_interfaces__srv__GetGoal_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { irob_interfaces__srv__GetGoal_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetGoal_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetGoal_Response where Self: Sized {
  const TYPE_NAME: &'static str = "irob_interfaces/srv/GetGoal_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__irob_interfaces__srv__GetGoal_Response() }
  }
}


#[link(name = "irob_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__irob_interfaces__srv__Activate_Request() -> *const std::ffi::c_void;
}

#[link(name = "irob_interfaces__rosidl_generator_c")]
extern "C" {
    fn irob_interfaces__srv__Activate_Request__init(msg: *mut Activate_Request) -> bool;
    fn irob_interfaces__srv__Activate_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Activate_Request>, size: usize) -> bool;
    fn irob_interfaces__srv__Activate_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Activate_Request>);
    fn irob_interfaces__srv__Activate_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Activate_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<Activate_Request>) -> bool;
}

// Corresponds to irob_interfaces__srv__Activate_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Activate_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for Activate_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !irob_interfaces__srv__Activate_Request__init(&mut msg as *mut _) {
        panic!("Call to irob_interfaces__srv__Activate_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Activate_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { irob_interfaces__srv__Activate_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { irob_interfaces__srv__Activate_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { irob_interfaces__srv__Activate_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Activate_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Activate_Request where Self: Sized {
  const TYPE_NAME: &'static str = "irob_interfaces/srv/Activate_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__irob_interfaces__srv__Activate_Request() }
  }
}


#[link(name = "irob_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__irob_interfaces__srv__Activate_Response() -> *const std::ffi::c_void;
}

#[link(name = "irob_interfaces__rosidl_generator_c")]
extern "C" {
    fn irob_interfaces__srv__Activate_Response__init(msg: *mut Activate_Response) -> bool;
    fn irob_interfaces__srv__Activate_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Activate_Response>, size: usize) -> bool;
    fn irob_interfaces__srv__Activate_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Activate_Response>);
    fn irob_interfaces__srv__Activate_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Activate_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<Activate_Response>) -> bool;
}

// Corresponds to irob_interfaces__srv__Activate_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Activate_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for Activate_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !irob_interfaces__srv__Activate_Response__init(&mut msg as *mut _) {
        panic!("Call to irob_interfaces__srv__Activate_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Activate_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { irob_interfaces__srv__Activate_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { irob_interfaces__srv__Activate_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { irob_interfaces__srv__Activate_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Activate_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Activate_Response where Self: Sized {
  const TYPE_NAME: &'static str = "irob_interfaces/srv/Activate_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__irob_interfaces__srv__Activate_Response() }
  }
}


#[link(name = "irob_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__irob_interfaces__srv__Deactivate_Request() -> *const std::ffi::c_void;
}

#[link(name = "irob_interfaces__rosidl_generator_c")]
extern "C" {
    fn irob_interfaces__srv__Deactivate_Request__init(msg: *mut Deactivate_Request) -> bool;
    fn irob_interfaces__srv__Deactivate_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Deactivate_Request>, size: usize) -> bool;
    fn irob_interfaces__srv__Deactivate_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Deactivate_Request>);
    fn irob_interfaces__srv__Deactivate_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Deactivate_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<Deactivate_Request>) -> bool;
}

// Corresponds to irob_interfaces__srv__Deactivate_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Deactivate_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for Deactivate_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !irob_interfaces__srv__Deactivate_Request__init(&mut msg as *mut _) {
        panic!("Call to irob_interfaces__srv__Deactivate_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Deactivate_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { irob_interfaces__srv__Deactivate_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { irob_interfaces__srv__Deactivate_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { irob_interfaces__srv__Deactivate_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Deactivate_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Deactivate_Request where Self: Sized {
  const TYPE_NAME: &'static str = "irob_interfaces/srv/Deactivate_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__irob_interfaces__srv__Deactivate_Request() }
  }
}


#[link(name = "irob_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__irob_interfaces__srv__Deactivate_Response() -> *const std::ffi::c_void;
}

#[link(name = "irob_interfaces__rosidl_generator_c")]
extern "C" {
    fn irob_interfaces__srv__Deactivate_Response__init(msg: *mut Deactivate_Response) -> bool;
    fn irob_interfaces__srv__Deactivate_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Deactivate_Response>, size: usize) -> bool;
    fn irob_interfaces__srv__Deactivate_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Deactivate_Response>);
    fn irob_interfaces__srv__Deactivate_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Deactivate_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<Deactivate_Response>) -> bool;
}

// Corresponds to irob_interfaces__srv__Deactivate_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Deactivate_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for Deactivate_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !irob_interfaces__srv__Deactivate_Response__init(&mut msg as *mut _) {
        panic!("Call to irob_interfaces__srv__Deactivate_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Deactivate_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { irob_interfaces__srv__Deactivate_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { irob_interfaces__srv__Deactivate_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { irob_interfaces__srv__Deactivate_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Deactivate_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Deactivate_Response where Self: Sized {
  const TYPE_NAME: &'static str = "irob_interfaces/srv/Deactivate_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__irob_interfaces__srv__Deactivate_Response() }
  }
}


#[link(name = "irob_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__irob_interfaces__srv__AtGoal_Request() -> *const std::ffi::c_void;
}

#[link(name = "irob_interfaces__rosidl_generator_c")]
extern "C" {
    fn irob_interfaces__srv__AtGoal_Request__init(msg: *mut AtGoal_Request) -> bool;
    fn irob_interfaces__srv__AtGoal_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<AtGoal_Request>, size: usize) -> bool;
    fn irob_interfaces__srv__AtGoal_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<AtGoal_Request>);
    fn irob_interfaces__srv__AtGoal_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<AtGoal_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<AtGoal_Request>) -> bool;
}

// Corresponds to irob_interfaces__srv__AtGoal_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct AtGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for AtGoal_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !irob_interfaces__srv__AtGoal_Request__init(&mut msg as *mut _) {
        panic!("Call to irob_interfaces__srv__AtGoal_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for AtGoal_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { irob_interfaces__srv__AtGoal_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { irob_interfaces__srv__AtGoal_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { irob_interfaces__srv__AtGoal_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for AtGoal_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for AtGoal_Request where Self: Sized {
  const TYPE_NAME: &'static str = "irob_interfaces/srv/AtGoal_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__irob_interfaces__srv__AtGoal_Request() }
  }
}


#[link(name = "irob_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__irob_interfaces__srv__AtGoal_Response() -> *const std::ffi::c_void;
}

#[link(name = "irob_interfaces__rosidl_generator_c")]
extern "C" {
    fn irob_interfaces__srv__AtGoal_Response__init(msg: *mut AtGoal_Response) -> bool;
    fn irob_interfaces__srv__AtGoal_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<AtGoal_Response>, size: usize) -> bool;
    fn irob_interfaces__srv__AtGoal_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<AtGoal_Response>);
    fn irob_interfaces__srv__AtGoal_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<AtGoal_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<AtGoal_Response>) -> bool;
}

// Corresponds to irob_interfaces__srv__AtGoal_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct AtGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for AtGoal_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !irob_interfaces__srv__AtGoal_Response__init(&mut msg as *mut _) {
        panic!("Call to irob_interfaces__srv__AtGoal_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for AtGoal_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { irob_interfaces__srv__AtGoal_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { irob_interfaces__srv__AtGoal_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { irob_interfaces__srv__AtGoal_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for AtGoal_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for AtGoal_Response where Self: Sized {
  const TYPE_NAME: &'static str = "irob_interfaces/srv/AtGoal_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__irob_interfaces__srv__AtGoal_Response() }
  }
}






#[link(name = "irob_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__irob_interfaces__srv__GetGoal() -> *const std::ffi::c_void;
}

// Corresponds to irob_interfaces__srv__GetGoal
#[allow(missing_docs, non_camel_case_types)]
pub struct GetGoal;

impl rosidl_runtime_rs::Service for GetGoal {
    type Request = GetGoal_Request;
    type Response = GetGoal_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__irob_interfaces__srv__GetGoal() }
    }
}




#[link(name = "irob_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__irob_interfaces__srv__Activate() -> *const std::ffi::c_void;
}

// Corresponds to irob_interfaces__srv__Activate
#[allow(missing_docs, non_camel_case_types)]
pub struct Activate;

impl rosidl_runtime_rs::Service for Activate {
    type Request = Activate_Request;
    type Response = Activate_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__irob_interfaces__srv__Activate() }
    }
}




#[link(name = "irob_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__irob_interfaces__srv__Deactivate() -> *const std::ffi::c_void;
}

// Corresponds to irob_interfaces__srv__Deactivate
#[allow(missing_docs, non_camel_case_types)]
pub struct Deactivate;

impl rosidl_runtime_rs::Service for Deactivate {
    type Request = Deactivate_Request;
    type Response = Deactivate_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__irob_interfaces__srv__Deactivate() }
    }
}




#[link(name = "irob_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__irob_interfaces__srv__AtGoal() -> *const std::ffi::c_void;
}

// Corresponds to irob_interfaces__srv__AtGoal
#[allow(missing_docs, non_camel_case_types)]
pub struct AtGoal;

impl rosidl_runtime_rs::Service for AtGoal {
    type Request = AtGoal_Request;
    type Response = AtGoal_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__irob_interfaces__srv__AtGoal() }
    }
}


