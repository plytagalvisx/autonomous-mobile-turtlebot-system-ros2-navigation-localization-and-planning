// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from irob_interfaces:srv/Deactivate.idl
// generated code does not contain a copyright notice

#ifndef IROB_INTERFACES__SRV__DETAIL__DEACTIVATE__TRAITS_HPP_
#define IROB_INTERFACES__SRV__DETAIL__DEACTIVATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "irob_interfaces/srv/detail/deactivate__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace irob_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const Deactivate_Request & msg,
  std::ostream & out)
{
  (void)msg;
  out << "null";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Deactivate_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  (void)msg;
  (void)indentation;
  out << "null\n";
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Deactivate_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace irob_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use irob_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const irob_interfaces::srv::Deactivate_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  irob_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use irob_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const irob_interfaces::srv::Deactivate_Request & msg)
{
  return irob_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<irob_interfaces::srv::Deactivate_Request>()
{
  return "irob_interfaces::srv::Deactivate_Request";
}

template<>
inline const char * name<irob_interfaces::srv::Deactivate_Request>()
{
  return "irob_interfaces/srv/Deactivate_Request";
}

template<>
struct has_fixed_size<irob_interfaces::srv::Deactivate_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<irob_interfaces::srv::Deactivate_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<irob_interfaces::srv::Deactivate_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace irob_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const Deactivate_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Deactivate_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Deactivate_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace irob_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use irob_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const irob_interfaces::srv::Deactivate_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  irob_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use irob_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const irob_interfaces::srv::Deactivate_Response & msg)
{
  return irob_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<irob_interfaces::srv::Deactivate_Response>()
{
  return "irob_interfaces::srv::Deactivate_Response";
}

template<>
inline const char * name<irob_interfaces::srv::Deactivate_Response>()
{
  return "irob_interfaces/srv/Deactivate_Response";
}

template<>
struct has_fixed_size<irob_interfaces::srv::Deactivate_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<irob_interfaces::srv::Deactivate_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<irob_interfaces::srv::Deactivate_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<irob_interfaces::srv::Deactivate>()
{
  return "irob_interfaces::srv::Deactivate";
}

template<>
inline const char * name<irob_interfaces::srv::Deactivate>()
{
  return "irob_interfaces/srv/Deactivate";
}

template<>
struct has_fixed_size<irob_interfaces::srv::Deactivate>
  : std::integral_constant<
    bool,
    has_fixed_size<irob_interfaces::srv::Deactivate_Request>::value &&
    has_fixed_size<irob_interfaces::srv::Deactivate_Response>::value
  >
{
};

template<>
struct has_bounded_size<irob_interfaces::srv::Deactivate>
  : std::integral_constant<
    bool,
    has_bounded_size<irob_interfaces::srv::Deactivate_Request>::value &&
    has_bounded_size<irob_interfaces::srv::Deactivate_Response>::value
  >
{
};

template<>
struct is_service<irob_interfaces::srv::Deactivate>
  : std::true_type
{
};

template<>
struct is_service_request<irob_interfaces::srv::Deactivate_Request>
  : std::true_type
{
};

template<>
struct is_service_response<irob_interfaces::srv::Deactivate_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // IROB_INTERFACES__SRV__DETAIL__DEACTIVATE__TRAITS_HPP_
